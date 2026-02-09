package edu.washington.cs.knowitall.util;

import com.sun.net.httpserver.HttpServer;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;
import java.util.concurrent.Executors;

import edu.washington.cs.knowitall.extractor.ExtractorException;
import edu.washington.cs.knowitall.extractor.ReVerbExtractor;
import edu.washington.cs.knowitall.extractor.ReVerbRelationExtractor;
import edu.washington.cs.knowitall.extractor.conf.ConfidenceFunction;
import edu.washington.cs.knowitall.extractor.conf.ReVerbOpenNlpConfFunction;
import edu.washington.cs.knowitall.nlp.ChunkedSentence;
import edu.washington.cs.knowitall.nlp.ChunkedSentenceIterator;
import edu.washington.cs.knowitall.nlp.ChunkedSentenceReader;
import edu.washington.cs.knowitall.nlp.extraction.ChunkedBinaryExtraction;
import edu.washington.cs.knowitall.normalization.BinaryExtractionNormalizer;
import edu.washington.cs.knowitall.normalization.NormalizedBinaryExtraction;

/**
 * Simple HTTP server wrapper for ReVerb extractor.
 * Exposes the extraction functionality via a REST API on port 42122.
 */
public class ReVerbHttpServer {

    private static final int PORT = 42122;

    private final ReVerbRelationExtractor extractor;
    private final ConfidenceFunction confFunc;
    private final BinaryExtractionNormalizer normalizer;

    public ReVerbHttpServer() throws ExtractorException {
        try {
            // Initialize the extractor
            this.extractor = new ReVerbExtractor(20, true, true, false);
            this.confFunc = new ReVerbOpenNlpConfFunction();
            this.normalizer = new BinaryExtractionNormalizer();

            // Initialize NLP tools
            DefaultObjects.initializeNlpTools();

            System.err.println("ReVerb HTTP Server initialized successfully.");
        } catch (IOException e) {
            throw new ExtractorException("Failed to initialize NLP tools", e);
        }
    }

    public void start() throws IOException {
        HttpServer server = HttpServer.create(new InetSocketAddress(PORT), 0);
        server.createContext("/", this::handleRoot);
        server.createContext("/extract", this::handleExtract);
        server.createContext("/health", this::handleHealth);
        server.setExecutor(Executors.newFixedThreadPool(4));
        server.start();
        System.err.println("ReVerb HTTP Server started on port " + PORT);
        System.err.println("Endpoints:");
        System.err.println("  GET / - Service info");
        System.err.println("  GET/POST /health - Health check");
        System.err.println("  POST /extract - Extract relations from text");
    }

    private void handleRoot(com.sun.net.httpserver.HttpExchange exchange) throws IOException {
        String response = "{\"service\":\"ReVerb\",\"status\":\"running\",\"endpoints\":{\"/health\":\"GET/POST\",\"/extract\":\"POST\"}}";
        sendJsonResponse(exchange, 200, response);
    }

    private void handleHealth(com.sun.net.httpserver.HttpExchange exchange) throws IOException {
        String response = "{\"status\":\"healthy\"}";
        sendJsonResponse(exchange, 200, response);
    }

    private void handleExtract(com.sun.net.httpserver.HttpExchange exchange) throws IOException {
        // Only accept POST requests
        if (!"POST".equalsIgnoreCase(exchange.getRequestMethod())) {
            sendJsonResponse(exchange, 405, "{\"error\":\"Method not allowed. Use POST.\"}");
            return;
        }

        try {
            // Read the request body
            String text = readRequestBody(exchange);

            // Process the text
            String result = extractFromText(text);

            // Return the result as JSON
            String jsonResponse = "{\"text\":\"" + escapeJson(text) + "\",\"extractions\":" + result + "}";
            sendJsonResponse(exchange, 200, jsonResponse);
        } catch (Exception e) {
            String errorResponse = "{\"error\":\"" + escapeJson(e.getMessage()) + "\"}";
            sendJsonResponse(exchange, 500, errorResponse);
        }
    }

    private String extractFromText(String text) throws IOException, ExtractorException {
        // Create a simple sentence reader that treats each line as a sentence
        java.io.ByteArrayInputStream bais = new java.io.ByteArrayInputStream(text.getBytes(StandardCharsets.UTF_8));
        java.io.BufferedReader reader = new java.io.BufferedReader(new java.io.InputStreamReader(bais, StandardCharsets.UTF_8));

        ChunkedSentenceReader sentenceReader = DefaultObjects.getDefaultSentenceReader(reader);
        ChunkedSentenceIterator sentenceIt = sentenceReader.iterator();

        StringBuilder sb = new StringBuilder();
        sb.append("[");

        boolean first = true;
        while (sentenceIt.hasNext()) {
            ChunkedSentence sent = sentenceIt.next();

            Iterable<ChunkedBinaryExtraction> extractions = extractor.extract(sent);

            for (ChunkedBinaryExtraction extr : extractions) {
                if (!first) {
                    sb.append(",");
                }
                first = false;

                double conf = confFunc.getConf(extr);
                NormalizedBinaryExtraction extrNorm = normalizer.normalize(extr);

                sb.append("{");
                sb.append("\"arg1\":\"").append(escapeJson(extrNorm.getArgument1().toString())).append("\",");
                sb.append("\"rel\":\"").append(escapeJson(extrNorm.getRelation().toString())).append("\",");
                sb.append("\"arg2\":\"").append(escapeJson(extrNorm.getArgument2().toString())).append("\",");
                sb.append("\"confidence\":").append(conf);
                sb.append("}");
            }
        }

        sb.append("]");
        return sb.toString();
    }

    private String readRequestBody(com.sun.net.httpserver.HttpExchange exchange) throws IOException {
        try (InputStream is = exchange.getRequestBody()) {
            return new String(is.readAllBytes(), StandardCharsets.UTF_8);
        }
    }

    private void sendJsonResponse(com.sun.net.httpserver.HttpExchange exchange, int statusCode, String json) throws IOException {
        byte[] responseBytes = json.getBytes(StandardCharsets.UTF_8);
        exchange.getResponseHeaders().set("Content-Type", "application/json");
        exchange.sendResponseHeaders(statusCode, responseBytes.length);
        try (OutputStream os = exchange.getResponseBody()) {
            os.write(responseBytes);
        }
    }

    private String escapeJson(String s) {
        if (s == null) return "";
        return s.replace("\\", "\\\\")
                .replace("\"", "\\\"")
                .replace("\n", "\\n")
                .replace("\r", "\\r")
                .replace("\t", "\\t");
    }

    public static void main(String[] args) {
        try {
            System.err.println("Starting ReVerb HTTP Server...");
            ReVerbHttpServer server = new ReVerbHttpServer();
            server.start();
            // Keep the main thread alive
            Thread.currentThread().join();
        } catch (Exception e) {
            System.err.println("Failed to start server: " + e.getMessage());
            e.printStackTrace();
            System.exit(1);
        }
    }
}