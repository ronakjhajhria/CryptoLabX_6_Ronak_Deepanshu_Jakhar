# Cryptocurrency Wallet - SAST Laboratory Assignment

## 1. Project Overview

This project implements a small console-based Cryptocurrency Wallet application using Python and SQLite.

The application is developed as part of the Static Application Security Testing (SAST) laboratory assignment. The purpose of the project is to demonstrate basic wallet functionalities and intentionally include security weaknesses that can be analyzed using the Semgrep SAST tool.

The application does not implement real cryptocurrency cryptography or blockchain functionality. It is only a simulation for educational and security-testing purposes.

---

## 2. Application Details

| Property | Details |
|---|---|
| Application | Cryptocurrency Wallet |
| Programming Language | Python |
| Database | SQLite |
| SAST Tool | Semgrep |
| SAST Version | 1.173.0 |
| Platform | Windows |
| Development Environment | Visual Studio Code |

---

## 3. Core Functionalities

The application provides the following functionalities:

1. User Registration
2. User Login
3. Wallet Creation
4. Balance Inquiry
5. Deposit
6. Transaction Request
7. Transaction History
8. Exit

---

## 4. Application Workflow

### User Registration

A new user can register using a username and password. After successful registration, a wallet is automatically created for the user with an initial balance of zero.

### User Login

Registered users can log in using their username and password.

### Wallet Creation

The application allows the logged-in user to create a wallet if one does not already exist.

### Balance Inquiry

The logged-in user can view the current wallet balance.

### Deposit

Users can deposit money into their wallet.

### Transaction Request

A logged-in user can transfer an amount to another user's wallet using the receiver's user ID.

### Transaction History

The application displays transaction records associated with a specified user ID.

---

## 5. Project Structure

```text
secure_application/
│
├── src/
│   └── vulnerable_app.py
│
├── reports/
│   └── SAST_Report.md
│
├── screenshots/
│
├── sast/
│
├── outputs/
│   ├── sast_lab_log.txt
│   └── semgrep_results.txt
│
├── testcases/
│
└── README.md