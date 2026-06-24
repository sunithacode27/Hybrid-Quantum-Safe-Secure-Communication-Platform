# Hybrid Quantum-Safe Secure Communication Platform

## Overview
The Hybrid Quantum-Safe Secure Communication Platform is a secure chat and file transfer application that combines Post-Quantum Cryptography (PQC) with AES encryption to provide secure communication against future quantum computing threats.
The project demonstrates how Kyber (ML-KEM-768), a NIST-selected post-quantum cryptographic algorithm, can be integrated with AES encryption to create a hybrid security model for secure messaging and file transfer.


## Problem Statement

Traditional public-key cryptographic algorithms such as RSA and ECC are vulnerable to quantum attacks. With the advancement of quantum computing, secure communication systems must adopt post-quantum cryptographic techniques.
This project addresses this challenge by implementing a hybrid communication platform that uses:
* Kyber (ML-KEM-768) for quantum-resistant key exchange
* AES for fast and secure message encryption
* HMAC-SHA256 for message integrity verification



## Objectives:

### Objective 1

Develop a hybrid cryptographic system by combining classical cryptography and post-quantum cryptography techniques to provide secure communication against quantum attacks.

### Objective 2

Analyze and redesign a hybrid cryptographic system by integrating classical cryptography with post-quantum techniques.

### Objective 3

Ensure strong quantum-resistant security with efficient and accurate key exchange, fast key generation, and reliable performance for future secure communication.



## Features

* Secure chat application
* Secure file transfer
* Image transfer with preview
* AES encryption
* HMAC integrity verification
* SQLite chat history storage
* Kyber (ML-KEM-768) post-quantum key exchange
* Performance benchmarking
* Graphical performance analysis



## Technologies Used

### Programming Language

* Python

### Cryptography Libraries

* pqcrypto
* pycryptodome

### Database

* SQLite3

### GUI

* Tkinter

### Data Visualization

* Pandas
* Matplotlib



## Project Structure

```text
quantum_safe_crypto_project1/

├── chat_gui.py
├── chat1_gui.py
├── server.py
├── crypto_utils.py
├── kyber_real_demo.py
├── hybrid_demo.py
├── benchmark.py
├── plot_graph.py
├── database.py
├── sender.py
├── receiver.py
├── chat.db
├── performance_results.csv
└── README.md
```



## Security Workflow

```text
Sender
   ↓
Kyber Key Exchange
   ↓
Shared Secret Generation
   ↓
AES Encryption
   ↓
Secure Message/File Transfer
   ↓
Receiver
```



## Performance Analysis

The system measures:

* Key Generation Time
* Encapsulation Time
* Decapsulation Time

Sample Results:

| Operation      | Time (seconds) |
| -------------- | -------------- |
| Key Generation | 0.003899       |
| Encapsulation  | 0.000729       |
| Decapsulation  | 0.000117       |






## Results

* Successfully implemented secure chat communication.
* Successfully implemented encrypted file transfer.
* Successfully integrated Kyber (ML-KEM-768).
* Successfully generated performance benchmark reports.
* Successfully visualized cryptographic performance using graphs.




## Future Enhancements

* Real network-based Kyber key exchange
* Multi-user secure chat
* Voice messaging
* Group communication
* Cloud deployment
* Secure key management server





## Conclusion

This project demonstrates the practical integration of Post-Quantum Cryptography with AES-based encryption to build a secure communication platform capable of resisting future quantum attacks. The implementation successfully achieves secure messaging, encrypted file transfer, integrity verification, and performance analysis while maintaining usability and efficiency.



## Authors

Developed as an academic project for secure and quantum-safe communication research.
