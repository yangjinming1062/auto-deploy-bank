/**
 * Script to create test user accounts for the Homarr dashboard application.
 *
 * Usage: pnpm run create-test-accounts
 *
 * This script creates:
 * - An admin user with full permissions
 * - A normal user with standard permissions
 */

import "dotenv/config";

import bcrypt from "bcrypt";
import { createDb } from "@homarr/core/infrastructure/db";
import { createId } from "@homarr/common";

import { schema } from "../packages/db/schema/index.js";

const DB_DRIVER = process.env.DB_DRIVER ?? "better-sqlite3";
const DB_URL = process.env.DB_URL ?? "./data.db";

async function createSaltAsync() {
  return bcrypt.genSalt(10);
}

async function hashPasswordAsync(password: string, salt: string) {
  return bcrypt.hash(password, salt);
}

async function getMaxGroupPositionAsync(db: Awaited<ReturnType<typeof createDb>>): Promise<number> {
  const result = await db.select({ position: schema.groups.position }).from(schema.groups).orderBy(schema.groups.position.desc()).limit(1);
  return result[0]?.position ?? 0;
}

async function createTestAccounts() {
  console.log("Initializing database connection...");

  const db = createDb(schema);

  console.log(`Connected to database (driver: ${DB_DRIVER})`);

  // Test account credentials
  const adminUser = {
    username: "admin",
    password: "Admin@123",
    email: "admin@example.com",
  };

  const normalUser = {
    username: "testuser",
    password: "User@123",
    email: "testuser@example.com",
  };

  // Create admin user
  console.log(`\nCreating admin user: ${adminUser.username}`);

  const adminSalt = await createSaltAsync();
  const adminHashedPassword = await hashPasswordAsync(adminUser.password, adminSalt);
  const adminUserId = createId();

  // Check if admin user already exists
  const existingAdmin = await db.query.users.findFirst({
    where: (users, { eq }) => eq(users.name, adminUser.username),
  });

  if (existingAdmin) {
    console.log(`Admin user "${adminUser.username}" already exists. Updating password...`);
    await db.update(schema.users)
      .set({ password: adminHashedPassword, salt: adminSalt })
      .where((users, { eq }) => eq(users.id, existingAdmin.id));
  } else {
    await db.insert(schema.users).values({
      id: adminUserId,
      name: adminUser.username,
      email: adminUser.email,
      password: adminHashedPassword,
      salt: adminSalt,
      provider: "credentials",
    });
    console.log(`Admin user created with ID: ${adminUserId}`);
  }

  // Create admin group with "admin" permission
  const adminGroupId = createId();
  const existingAdminGroup = await db.query.groups.findFirst({
    where: (groups, { eq }) => eq(groups.name, "credentials-admin"),
  });

  if (existingAdminGroup) {
    console.log(`Admin group "credentials-admin" already exists.`);
  } else {
    const maxPosition = await getMaxGroupPositionAsync(db);
    await db.insert(schema.groups).values({
      id: adminGroupId,
      name: "credentials-admin",
      ownerId: adminUserId,
      position: maxPosition + 1,
    });
    console.log(`Admin group created with ID: ${adminGroupId}`);
  }

  // Get the admin group ID (either existing or new)
  const adminGroup = await db.query.groups.findFirst({
    where: (groups, { eq }) => eq(groups.name, "credentials-admin"),
  });

  if (!adminGroup) {
    throw new Error("Failed to find or create admin group");
  }

  // Check if admin permission already exists for the group
  const existingAdminPermission = await db.query.groupPermissions.findFirst({
    where: (groupPermissions, { eq, and }) =>
      and(eq(groupPermissions.groupId, adminGroup.id), eq(groupPermissions.permission, "admin" as any)),
  });

  if (!existingAdminPermission) {
    await db.insert(schema.groupPermissions).values({
      groupId: adminGroup.id,
      permission: "admin" as any,
    });
    console.log("Admin permission added to admin group");
  }

  // Ensure admin user is a member of admin group
  const existingAdminMembership = await db.query.groupMembers.findFirst({
    where: (groupMembers, { eq, and }) =>
      and(eq(groupMembers.groupId, adminGroup.id), eq(groupMembers.userId, adminUserId)),
  });

  if (!existingAdminMembership) {
    await db.insert(schema.groupMembers).values({
      groupId: adminGroup.id,
      userId: adminUserId,
    });
    console.log("Admin user added to admin group");
  }

  // Create normal user
  console.log(`\nCreating normal user: ${normalUser.username}`);

  const normalSalt = await createSaltAsync();
  const normalHashedPassword = await hashPasswordAsync(normalUser.password, normalSalt);
  const normalUserId = createId();

  // Check if normal user already exists
  const existingNormalUser = await db.query.users.findFirst({
    where: (users, { eq }) => eq(users.name, normalUser.username),
  });

  if (existingNormalUser) {
    console.log(`Normal user "${normalUser.username}" already exists. Updating password...`);
    await db.update(schema.users)
      .set({ password: normalHashedPassword, salt: normalSalt })
      .where((users, { eq }) => eq(users.id, existingNormalUser.id));
  } else {
    await db.insert(schema.users).values({
      id: normalUserId,
      name: normalUser.username,
      email: normalUser.email,
      password: normalHashedPassword,
      salt: normalSalt,
      provider: "credentials",
    });
    console.log(`Normal user created with ID: ${normalUserId}`);
  }

  console.log("\n========================================");
  console.log("Test accounts created successfully!");
  console.log("========================================");
  console.log("\nAdmin Account:");
  console.log(`  Username: ${adminUser.username}`);
  console.log(`  Password: ${adminUser.password}`);
  console.log(`  Login URL: /auth/login`);
  console.log("\nNormal User Account:");
  console.log(`  Username: ${normalUser.username}`);
  console.log(`  Password: ${normalUser.password}`);
  console.log(`  Login URL: /auth/login`);
  console.log("\n========================================");
}

createTestAccounts()
  .then(() => {
    console.log("\nDone!");
    process.exit(0);
  })
  .catch((error) => {
    console.error("Error creating test accounts:", error);
    process.exit(1);
  });