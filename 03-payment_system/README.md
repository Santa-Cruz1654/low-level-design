# Payment Gateway System

A Low-Level Design implementation of a payment processing system in Python.

This project focuses on designing a reliable, extensible, and testable payment
workflow using Object-Oriented Design, SOLID principles, design patterns,
state machines, idempotency, retries, reconciliation, repositories,
Unit of Work, and the Transactional Outbox pattern.

The implementation uses in-memory infrastructure so that the focus remains on
the architecture and low-level design rather than production infrastructure.

---

## 1. Problem Statement

Design a payment processing system that can:

- Accept payment requests
- Prevent duplicate payments
- Support multiple payment gateways
- Track the payment lifecycle
- Handle successful and failed payments
- Handle uncertain provider outcomes
- Retry transient failures
- Reconcile payments with unknown outcomes
- Persist payment events reliably
- Support concurrent updates safely
- Remain extensible for additional payment providers

---

# 2. High-Level Architecture

```text
                         Payment Request
                               |
                               v
                    +---------------------+
                    |  Payment Controller  |
                    +----------+----------+
                               |
                               v
                    +---------------------+
                    |   Application Layer  |
                    |   PaymentService     |
                    +----------+----------+
                               |
                +--------------+--------------+
                |                             |
                v                             v
        Idempotency Check              Payment Entity
                                              |
                                              v
                                      State Machine
                                              |
                                              v
                                       GatewayFactory
                                              |
                              +---------------+---------------+
                              |                               |
                              v                               v
                           Paytm                          Razorpay
                              |                               |
                              +---------------+---------------+
                                              |
                                              v
                                       RetryExecutor
                                              |
                                              v
                                      Provider Response
                                              |
                         +--------------------+--------------------+
                         |                    |                    |
                         v                    v                    v
                      SUCCESS              FAILED              UNKNOWN
                         |                    |                    |
                         |                    |                    v
                         |                    |              Reconciliation
                         |                    |                    |
                         |                    |            +-------+-------+
                         |                    |            |               |
                         |                    |            v               v
                         |                    |         SUCCESS          FAILED
                         |                    |            |               |
                         +--------------------+------------+---------------+
                                              |
                                              v
                                        Outbox Event
                                              |
                                              v
                                      Message Publisher