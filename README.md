# Software Engineering & Robotics Curriculum

This repository contains a structured, hands-on curriculum designed to transition learners from basic programming concepts to advanced software engineering, machine learning, and robotic control systems (ROS2).

The methodology relies strictly on **Test-Driven Development (TDD)**. Each module consists of unit tests defining the expected behavior of the code, requiring the implementation of logic to satisfy these requirements. This ensures a deep understanding of implementation patterns and quality assurance.

## Curriculum Structure

The codebase is organized into specialized domains, progressing in complexity and abstraction.

### I. Core Foundation
*   **01_Python_Zaklady**: Language syntax, memory management, type system, Python internals.
*   **02_OOP**: Object-Oriented Design, SOLID principles, Abstract Base Classes (ABC), Composition.
*   **03_Datove_Struktury_Algoritmy**: Computational complexity (Big O), graph algorithms, data structure optimization.

### II. Engineering Practices
*   **04_Git_a_Workflow**: Version control strategies (Git Flow), CI/CD pipelines, code review standards.
*   **05_Testing**: Unit testing (pytest), integration testing, mocking, and coverage analysis.
*   **06_Cteni_a_Debugovani_Kodu**: Static analysis, profiling, debugging techniques, legacy code refactoring.

### III. Data Science & Artificial Intelligence
*   **07_Numpy_a_Matematika**: Linear algebra, statistical modeling, numerical computing optimization.
*   **08_Machine_Learning**: Supervised/Unsupervised learning, Neural Networks, PyTorch implementation.
*   **09_Computer_Vision**: Image processing pipelines, OpenCV, feature detection, 3D reconstruction.

### IV. Robotics & Systems
*   **10_ROS2**: Robot Operating System architecture, DDS middleware, navigation stack, perception.
*   **11_Linux_a_Terminal**: Shell scripting, process management, kernel interaction.
*   **12_Networking_a_API**: TCP/UDP protocols, REST/WebSockets, asynchronous communication.
*   **13_Paralelismus_a_Async**: Concurrency models, multiprocessing, threading, unlocking the GIL.

## Methodology & Workflow

This project eschews passive learning in favor of active implementation.

1.  **Analysis**: Review the provided interface and documentation strings in the problem files.
2.  **Implementation**: Write the logic to satisfy the functional requirements (marked by `TODO` directives).
3.  **Verification**: Execute the test suite using the provided runner to validate correctness, edge cases, and type safety.

## Getting Started

### Prerequisites
*   Python 3.8+
*   Git
*   (Optional) Docker for ROS2 modules

### Installation

```bash
git clone git@github.com:stpnkis/Programming_tutorial.git
cd Programming_tutorial

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Execute core runner
python3 start.py
```

## License

This project is open-source and available under the **MIT License**.

---
*Maintained by Stepan Kis*
