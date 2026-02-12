/**
 * Account Creation Script for DoraCMS
 * Creates admin and normal user accounts
 */

var mongoose = require('mongoose');
var crypto = require("crypto");
var shortid = require('shortid');

// Load settings
var settings = require("./models/db/settings");

// Connect to MongoDB
mongoose.connect(settings.URL);

// Define schemas
var Schema = mongoose.Schema;

var UserSchema = new Schema({
    _id: { type: String, unique: true, 'default': shortid.generate },
    name: String,
    userName: String,
    password: String,
    email: String,
    qq: Number,
    phoneNum: Number,
    comments: { type: String, default: "这个人很懒，什么都没有留下..." },
    position: String,
    company: String,
    website: String,
    date: { type: Date, default: Date.now },
    logo: { type: String, default: "/upload/images/defaultlogo.png" },
    group: { type: String, default: "0" },
    gender: String,
    province: String,
    city: String,
    year: Number,
    openid: String,
    retrieve_time: Number
});

var AdminGroupSchema = new Schema({
    _id: { type: String, unique: true, 'default': shortid.generate },
    name: String,
    comments: String,
    power: String,
    date: { type: Date, default: Date.now }
});

var AdminUserSchema = new Schema({
    _id: { type: String, unique: true, 'default': shortid.generate },
    name: String,
    userName: String,
    password: String,
    email: String,
    phoneNum: Number,
    comments: String,
    date: { type: Date, default: Date.now },
    logo: { type: String, default: "/upload/images/defaultlogo.png" },
    auth: { type: Boolean, default: false },
    group: { type: String, ref: 'AdminGroup' }
});

var User = mongoose.model("User", UserSchema);
var AdminGroup = mongoose.model("AdminGroup", AdminGroupSchema);
var AdminUser = mongoose.model("AdminUser", AdminUserSchema);

// Encryption function (matches DbOpt.encrypt)
function encrypt(data, key) {
    var cipher = crypto.createCipher("bf", key);
    var newPsd = "";
    newPsd += cipher.update(data, "utf8", "hex");
    newPsd += cipher.final("hex");
    return newPsd;
}

// Create admin group if not exists
function ensureAdminGroup(callback) {
    AdminGroup.findOne({ name: '超级管理员组' }, function(err, group) {
        if (err) {
            console.error('Error finding admin group:', err);
            return callback(err);
        }
        if (group) {
            console.log('Admin group already exists');
            return callback(null, group);
        }
        var newGroup = new AdminGroup({
            name: '超级管理员组',
            comments: '拥有所有权限的管理员组',
            power: '["sysTemManage","sysTemManage_user","sysTemManage_user_view","sysTemManage_user_add","sysTemManage_user_modify","sysTemManage_user_del","sysTemManage_uGroup","sysTemManage_uGroup_view","sysTemManage_uGroup_add","sysTemManage_uGroup_modify","sysTemManage_uGroup_del","sysTemManage_ads","sysTemManage_ads_view","sysTemManage_ads_add","sysTemManage_ads_modify","sysTemManage_ads_del","sysTemManage_files","sysTemManage_files_view","sysTemManage_files_add","sysTemManage_files_modify","sysTemManage_files_del","sysTemManage_data","sysTemManage_data_view","sysTemManage_data_1","sysTemManage_data_1_view","sysTemManage_data_1_backup","sysTemManage_data_1_del","sysTemManage_logs","sysTemManage_logs_view","contentManage","contentManage_content","contentManage_content_view","contentManage_content_add","contentManage_content_modify","contentManage_content_del","contentManage_content_push","contentManage_content_push_modify","contentManage_cateGory","contentManage_cateGory_view","contentManage_cateGory_add","contentManage_cateGory_modify","contentManage_cateGory_del","contentManage_tag","contentManage_tag_view","contentManage_tag_add","contentManage_tag_modify","contentManage_tag_del","contentManage_temp","contentManage_temp_view","contentManage_temp_add","contentManage_temp_modify","contentManage_temp_del","contentManage_temp_import","contentManage_tpItem","contentManage_tpItem_view","contentManage_tpItem_add","contentManage_tpItem_modify","contentManage_tpItem_del","contentManage_msg","contentManage_msg_view","contentManage_msg_add","contentManage_msg_modify","contentManage_msg_del","contentManage_notice","contentManage_notice_view","contentManage_notice_add","contentManage_notice_modify","contentManage_notice_del","contentManage_notice_1","contentManage_notice_1_view","contentManage_notice_1_add","contentManage_notice_1_modify","contentManage_notice_1_del","contentManage_notice_2","contentManage_notice_2_view","contentManage_notice_2_add","contentManage_notice_2_modify","contentManage_notice_2_del","contentManage_notice_3","contentManage_notice_3_view","contentManage_notice_3_add","contentManage_notice_3_modify","contentManage_notice_3_del","userManage","userManage_user","userManage_user_view","userManage_user_modify","userManage_user_del"]'
        });
        newGroup.save(function(err) {
            if (err) {
                console.error('Error creating admin group:', err);
                return callback(err);
            }
            console.log('Admin group created successfully');
            callback(null, newGroup);
        });
    });
}

// Create admin user
function createAdminUser(adminGroup, callback) {
    var adminUsername = 'admin';
    var adminPassword = 'Admin@123';
    var adminEmail = 'admin@example.com';

    AdminUser.findOne({ userName: adminUsername }, function(err, user) {
        if (err) {
            console.error('Error finding admin user:', err);
            return callback(err);
        }
        if (user) {
            console.log('Admin user already exists with username:', adminUsername);
            console.log('Admin login URL: /admin');
            return callback(null);
        }

        var encryptedPassword = encrypt(adminPassword, settings.encrypt_key);
        var newAdmin = new AdminUser({
            name: '系统管理员',
            userName: adminUsername,
            password: encryptedPassword,
            email: adminEmail,
            comments: '系统超级管理员',
            group: adminGroup._id
        });

        newAdmin.save(function(err) {
            if (err) {
                console.error('Error creating admin user:', err);
                return callback(err);
            }
            console.log('Admin user created successfully');
            console.log('  Username:', adminUsername);
            console.log('  Password:', adminPassword);
            console.log('  Login URL: /admin');
            callback(null);
        });
    });
}

// Create normal user
function createNormalUser(callback) {
    var normalUsername = 'testuser';
    var normalPassword = 'User@123';
    var normalEmail = 'testuser@example.com';

    User.findOne({ $or: [{ userName: normalUsername }, { email: normalEmail }] }, function(err, user) {
        if (err) {
            console.error('Error finding normal user:', err);
            return callback(err);
        }
        if (user) {
            console.log('Normal user already exists with username:', normalUsername);
            console.log('Normal user login URL: /users/login');
            return callback(null);
        }

        var encryptedPassword = encrypt(normalPassword, settings.encrypt_key);
        var newUser = new User({
            name: '测试用户',
            userName: normalUsername,
            password: encryptedPassword,
            email: normalEmail,
            comments: '用于安全测试的普通用户账户',
            company: '测试公司',
            position: '测试工程师'
        });

        newUser.save(function(err) {
            if (err) {
                console.error('Error creating normal user:', err);
                return callback(err);
            }
            console.log('Normal user created successfully');
            console.log('  Username:', normalUsername);
            console.log('  Password:', normalPassword);
            console.log('  Login URL: /users/login');
            callback(null);
        });
    });
}

// Main execution
console.log('=== DoraCMS Account Creation Script ===\n');

ensureAdminGroup(function(err, adminGroup) {
    if (err) {
        console.error('Failed to ensure admin group');
        process.exit(1);
    }

    createAdminUser(adminGroup, function(err) {
        if (err) {
            console.error('Failed to create admin user');
        }

        createNormalUser(function(err) {
            if (err) {
                console.error('Failed to create normal user');
            }

            console.log('\n=== Account Creation Complete ===');
            mongoose.disconnect();
            process.exit(0);
        });
    });
});