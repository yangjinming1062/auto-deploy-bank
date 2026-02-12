//go:build ignore

// Vikunja Account Creation Script
// This script creates admin and normal user accounts for security testing
//
// Usage: go run create_test_accounts.go
//
// Requirements:
// - A running Vikunja instance with database access
// - Configuration in config.yaml or environment variables set

package main

import (
	"fmt"
	"log"
	"os"

	"code.vikunja.io/api/pkg/config"
	"code.vikunja.io/api/pkg/db"
	"code.vikunja.io/api/pkg/models"
	"code.vikunja.io/api/pkg/user"
)

func main() {
	fmt.Println("=== Vikunja Test Account Creation Script ===")
	fmt.Println()

	// Initialize configuration
	config.InitConfig()
	config.InitDefaultConfig()

	// Initialize database
	engine, err := db.CreateDBEngine()
	if err != nil {
		log.Fatalf("Failed to create database engine: %v", err)
	}
	defer engine.Close()

	// Sync database schema
	err = engine.Sync2()
	if err != nil {
		log.Fatalf("Failed to sync database schema: %v", err)
	}

	session := db.NewSession()
	defer session.Close()

	// Create admin user
	fmt.Println("Creating admin account...")
	adminUser := &user.User{
		Username: "admin",
		Email:    "admin@test.local",
		Password: "Admin@123",
	}
	admin, err := user.CreateUser(session, adminUser)
	if err != nil {
		// Check if user already exists
		existingAdmin, getErr := user.GetUserByUsername(session, "admin")
		if getErr == nil {
			fmt.Printf("Admin user 'admin' already exists (ID: %d)\n", existingAdmin.ID)
			admin = existingAdmin
		} else {
			log.Printf("Warning creating admin user: %v", err)
		}
	} else {
		fmt.Printf("Admin user 'admin' created successfully (ID: %d)\n", admin.ID)

		// Create initial project for admin
		err = models.CreateNewProjectForUser(session, admin)
		if err != nil {
			log.Printf("Warning creating admin project: %v", err)
		}
	}

	// Create normal user
	fmt.Println("\nCreating normal user account...")
	normalUser := &user.User{
		Username: "testuser",
		Email:    "testuser@test.local",
		Password: "User@123",
	}
	normal, err := user.CreateUser(session, normalUser)
	if err != nil {
		// Check if user already exists
		existingUser, getErr := user.GetUserByUsername(session, "testuser")
		if getErr == nil {
			fmt.Printf("Normal user 'testuser' already exists (ID: %d)\n", existingUser.ID)
			normal = existingUser
		} else {
			log.Printf("Warning creating normal user: %v", err)
		}
	} else {
		fmt.Printf("Normal user 'testuser' created successfully (ID: %d)\n", normal.ID)

		// Create initial project for normal user
		err = models.CreateNewProjectForUser(session, normal)
		if err != nil {
			log.Printf("Warning creating normal user project: %v", err)
		}
	}

	// Commit transaction
	if err := session.Commit(); err != nil {
		log.Fatalf("Failed to commit transaction: %v", err)
	}

	fmt.Println()
	fmt.Println("=== Account Credentials ===")
	fmt.Println()
	fmt.Println("Admin Account:")
	fmt.Println("  Username: admin")
	fmt.Println("  Password: Admin@123")
	fmt.Println("  Login URL: /api/v1/login")
	fmt.Println()
	fmt.Println("Normal User Account:")
	fmt.Println("  Username: testuser")
	fmt.Println("  Password: User@123")
	fmt.Println("  Login URL: /api/v1/login")
	fmt.Println()
	fmt.Println("Login Request Example:")
	fmt.Println(`  POST /api/v1/login HTTP/1.1`)
	fmt.Println(`  Host: localhost:3456`)
	fmt.Println(`  Content-Type: application/json`)
	fmt.Println()
	fmt.Println(`  {`)
	fmt.Println(`    "username": "admin",`)
	fmt.Println(`    "password": "Admin@123"`)
	fmt.Println(`  }`)
	fmt.Println()
	fmt.Println("=== Script completed successfully ===")
}