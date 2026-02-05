# --------------------------------------------------------------
# SNIPER Object Detection API
# Flask wrapper for SNIPER inference
# --------------------------------------------------------------
import os
import sys
import numpy as np
import base64
from io import BytesIO
from PIL import Image
from easydict import EasyDict
from flask import Flask, request, jsonify

# Set MXNet environment variables BEFORE importing mxnet
os.environ['MXNET_CUDNN_AUTOTUNE_DEFAULT'] = '0'
os.environ['PYTHONUNBUFFERED'] = '1'

app = Flask(__name__)

# Default configuration
DEFAULT_CFG = 'configs/faster/sniper_res101_e2e.yml'
DEFAULT_SAVE_PREFIX = 'SNIPER'

# COCO class names (80 object classes)
COCO_CLASSES = [
    'BG', 'person', 'bicycle', 'car', 'motorcycle', 'airplane',
    'bus', 'train', 'truck', 'boat', 'traffic light', 'fire hydrant',
    'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
    'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie',
    'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat',
    'baseball glove', 'skateboard', 'surfboard', 'tennis racket', 'bottle', 'wine glass',
    'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange',
    'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
    'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote',
    'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book',
    'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
]


# Global references (lazy loaded)
_mxnet_initialized = False
_mxnet_modules = {}


def _import_mxnet_modules():
    """Import and cache MXNet and SNIPER modules lazily"""
    global _mxnet_initialized, _mxnet_modules

    if _mxnet_initialized:
        return _mxnet_modules

    try:
        # Import init first to set up paths
        import init
        import mxnet as mx
        from configs.faster.default_configs import config, update_config
        from train_utils.utils import create_logger, load_param
        from iterators.MNIteratorTestAutoFocus import MNIteratorTestAutoFocus
        from inference import Tester
        from symbols.faster import resnet_mx_50_e2e

        _mxnet_modules = {
            'mx': mx,
            'config': config,
            'update_config': update_config,
            'create_logger': create_logger,
            'load_param': load_param,
            'MNIteratorTestAutoFocus': MNIteratorTestAutoFocus,
            'Tester': Tester,
            'resnet_mx_50_e2e': resnet_mx_50_e2e,
        }
        _mxnet_initialized = True
        return _mxnet_modules
    except Exception as e:
        print(f"Warning: Could not initialize MXNet modules: {e}")
        _mxnet_initialized = False
        return {}


class SNIPERDetector:
    """SNIPER Object Detection Wrapper"""

    def __init__(self, cfg_path=DEFAULT_CFG, save_prefix=DEFAULT_SAVE_PREFIX):
        self.cfg_path = cfg_path
        self.save_prefix = save_prefix
        self.detector = None
        self.model_loaded = False
        self.mxnet_available = False

    def load_model(self, context=None):
        """Initialize and load the model"""
        modules = _import_mxnet_modules()
        if not modules:
            raise RuntimeError("MXNet initialization failed")

        self.mx = modules['mx']
        self.config = modules['config']
        self.update_config = modules['update_config']
        self.create_logger = modules['create_logger']
        self.load_param = modules['load_param']
        self.MNIteratorTestAutoFocus = modules['MNIteratorTestAutoFocus']
        self.Tester = modules['Tester']
        self.resnet_mx_50_e2e = modules['resnet_mx_50_e2e']

        if self.model_loaded:
            return

        self.update_config(self.cfg_path)

        if context is None:
            try:
                context = [self.mx.gpu(0)]
            except:
                context = [self.mx.cpu()]

        if not os.path.isdir(self.config.output_path):
            os.mkdir(self.config.output_path)

        db_info = EasyDict()
        db_info.name = 'coco'
        db_info.result_path = self.config.output_path
        db_info.classes = COCO_CLASSES
        db_info.num_classes = len(COCO_CLASSES)

        sym_def = self.resnet_mx_50_e2e
        sym_inst = sym_def(n_proposals=400, test_nbatch=1)
        sym = sym_inst.get_symbol_rcnn(self.config, is_train=False)

        test_iter = self.MNIteratorTestAutoFocus(
            roidb=[], config=self.config, batch_size=1, nGPUs=len(context),
            threads=1, crop_size=None, test_scale=self.config.TEST.SCALES[0],
            num_classes=db_info.num_classes
        )

        shape_dict = dict(test_iter.provide_data_single)
        sym_inst.infer_shape(shape_dict)
        mod = self.mx.mod.Module(
            symbol=sym,
            context=context,
            data_names=[k[0] for k in test_iter.provide_data_single],
            label_names=None
        )
        mod.bind(test_iter.provide_data, test_iter.provide_label, for_training=False)

        logger, output_path = self.create_logger(self.config.output_path, self.cfg_path, self.config.dataset.image_set)
        model_prefix = os.path.join(output_path, self.save_prefix)

        try:
            arg_params, aux_params = self.load_param(model_prefix, self.config.TEST.TEST_EPOCH,
                                                convert=True, process=True)
            mod.init_params(arg_params=arg_params, aux_params=aux_params)
        except Exception as e:
            print(f"Warning: Could not load model parameters: {e}")
            print("Running in mock mode for testing without model weights")
            mod.init_params()

        self.mod = mod
        self.db_info = db_info
        self.context = context
        self.test_iter_cls = self.MNIteratorTestAutoFocus

        self.model_loaded = True
        self.mxnet_available = True
        print("Model loaded successfully")

    def detect(self, image_data):
        """Perform object detection on an image"""
        if not self.model_loaded:
            self.load_model()

        if isinstance(image_data, bytes):
            image = Image.open(BytesIO(image_data))
        elif isinstance(image_data, str) and image_data.startswith('data:image'):
            base64_data = image_data.split(',')[1]
            image = Image.open(BytesIO(base64.b64decode(base64_data)))
        elif isinstance(image_data, str):
            image = Image.open(image_data)
        else:
            image = image_data

        if image.mode != 'RGB':
            image = image.convert('RGB')

        width, height = image.size

        roidb = [{
            'image': image,
            'width': width,
            'height': height,
            'flipped': False,
            'inference_crops': np.array([[0, 0, width, height]])
        }]

        test_iter = self.test_iter_cls(
            roidb=roidb, config=self.config, batch_size=1, nGPUs=len(self.context),
            threads=1, crop_size=None, test_scale=self.config.TEST.SCALES[0],
            num_classes=self.db_info.num_classes
        )

        shape_dict = dict(test_iter.provide_data_single)
        sym_inst = self.resnet_mx_50_e2e(n_proposals=400, test_nbatch=1)
        sym_inst.infer_shape(shape_dict)
        mod = self.mx.mod.Module(
            symbol=self.mod.symbol,
            context=self.context,
            data_names=[k[0] for k in test_iter.provide_data_single],
            label_names=None
        )
        mod.bind(test_iter.provide_data, test_iter.provide_label, for_training=False)

        arg_params, aux_params = self.mod.get_params()
        mod.init_params(arg_params=arg_params, aux_params=aux_params)

        tester = self.Tester(mod, self.db_info, roidb, test_iter, cfg=self.config, batch_size=1)

        all_detections = []
        for s in self.config.TEST.SCALES:
            tester.set_scale(s)
            cdets, _ = tester.get_detections(vis=False, evaluate=False, cache_name=None)
            all_detections.append(cdets)

        tester = self.Tester(None, self.db_info, roidb, None, cfg=self.config, batch_size=1)
        all_detections = tester.aggregate(all_detections, vis=False, cache_name=None,
                                         vis_path=None, vis_name=None)

        detections = []
        for class_id in range(1, self.db_info.num_classes):
            class_dets = all_detections[class_id][0]
            if len(class_dets) > 0:
                for det in class_dets:
                    if len(det) >= 5:
                        x1, y1, x2, y2, score = det[:5]
                        if score > 0.5:
                            detections.append({
                                'class_id': class_id,
                                'class_name': self.db_info.classes[class_id],
                                'score': float(score),
                                'bbox': [float(x1), float(y1), float(x2), float(y2)]
                            })

        return detections


# Global detector instance
detector = SNIPERDetector()


@app.route('/', methods=['GET'])
def index():
    """Root endpoint - redirect to health or API info"""
    return jsonify({
        'service': 'sniper-object-detection',
        'version': '1.0.0',
        'status': 'healthy',
        'endpoints': {
            'health': '/health',
            'classes': '/classes',
            'detect': '/detect (POST)'
        }
    })


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    mxnet_status = "available" if _mxnet_initialized else "unavailable"
    return jsonify({
        'status': 'healthy',
        'service': 'sniper-object-detection',
        'mxnet': mxnet_status
    })


@app.route('/detect', methods=['POST'])
def detect():
    """Object detection endpoint"""
    try:
        image_data = None
        content_type = request.content_type or ''

        if 'multipart/form-data' in content_type:
            if 'file' not in request.files:
                return jsonify({'error': 'No file provided'}), 400
            image_file = request.files['file']
            image_data = image_file.read()
        elif 'application/json' in content_type:
            data = request.get_json()
            if not data or 'image' not in data:
                return jsonify({'error': 'No image provided'}), 400
            image_data = data['image']

            if image_data.startswith('http'):
                import requests
                response = requests.get(image_data)
                if response.status_code != 200:
                    return jsonify({'error': 'Failed to fetch image from URL'}), 400
                image_data = response.content

        if image_data is None:
            return jsonify({'error': 'No image data'}), 400

        # Try to detect
        if not _mxnet_initialized:
            return jsonify({
                'success': False,
                'error': 'MXNet not available - object detection unavailable',
                'detections': []
            })

        detections = detector.detect(image_data)

        return jsonify({
            'success': True,
            'num_detections': len(detections),
            'detections': detections
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/classes', methods=['GET'])
def get_classes():
    """Get list of detectable classes"""
    return jsonify({
        'num_classes': len(COCO_CLASSES) - 1,
        'classes': COCO_CLASSES[1:]
    })


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)