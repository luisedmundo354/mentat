([Home | Mentat](https://luisedmundo354.github.io/mentat_website/#:~:text=Mentat%3A%20Transforming%20Medical%20Decision)) ([Home | Mentat](https://luisedmundo354.github.io/mentat_website/))  
# Mentat AI  
*Transforming Medical Decision-Making*  

## Introduction  
**Mentat AI** is an open-source, AI-driven system that streamlines medical data collection and supports clinical decision-making. It provides an end-to-end solution that automates patient data recording, information retrieval, and preliminary diagnostic insight generation using a small, efficient language model optimized for low-power GPUs ([Home | Mentat](https://luisedmundo354.github.io/mentat_website/#:~:text=Healthcare%20professionals%20manage%20the%20complex,power%20GPUs)). By running entirely offline with no reliance on cloud services, Mentat preserves patient data integrity and privacy, keeping all information within the local network ([Home | Mentat](https://luisedmundo354.github.io/mentat_website/#:~:text=This%20approach%20ensures%20secure%2C%20offline,servers%2C%20preserving%20patient%20data%20integrity)). This approach reduces transcription errors and saves clinicians time, allowing healthcare professionals to focus more on patient care.  

A key innovation of Mentat is its conversational interface for data gathering, coupled with intelligent analysis of the collected information. The system harnesses a lightweight large language model (LLM) to guide patient interviews and then produce a summary or diagnostic pointers augmented with relevant medical knowledge ([Home | Mentat](https://luisedmundo354.github.io/mentat_website/#:~:text=patient%20data%2C%20relying%20on%20systems,power%20GPUs)) ([Technology | Mentat](https://luisedmundo354.github.io/mentat_website/technology/#:~:text=1.%20Structured%20Data%20Retrieval%20,Augmented%20Generation%20%28RAG)). While Mentat provides advanced AI-driven insights, it is **not a standalone diagnostic tool** – it is designed to assist clinicians, and medical professionals remain the final authority on patient care decisions ([Technology | Mentat](https://luisedmundo354.github.io/mentat_website/technology/#:~:text=,on%20patient%20care%20and%20decisions)). This ensures that Mentat complements the expertise of doctors and nurses, enhancing decision-making without replacing it.  

## Technology Stack  
- **Python & Tkinter (GUI):** The core application is built in Python for rapid development and flexibility. It uses Tkinter to provide a simple cross-platform desktop GUI, allowing users to interact with Mentat through windows, forms, and dialogs.  
- **On-Device AI Models:** Mentat employs the **Phi-3.5 Mini** language model for natural language understanding and generation, deployed via **LlamaEdge** (a lightweight Rust/Wasm runtime for machine learning). This model – roughly equivalent to a distilled GPT-3.5 – runs locally on-device to handle conversation and reasoning tasks ([Technology | Mentat](https://luisedmundo354.github.io/mentat_website/technology/#:~:text=Mentat%20uses%20Phi%203,handle%20natural%20language%20tasks%20efficiently)). It supports a large context window (~32k tokens) for extensive dialogue memory, and it operates using the base model weights without additional fine-tuning ([Technology | Mentat](https://luisedmundo354.github.io/mentat_website/technology/#:~:text=,until%20it%20completes%20the%20data)).  
- **Data Storage:** All captured information is stored locally. In the current version, Mentat organizes the collected text into structured categories and saves it as JSON files for each patient ([Technology | Mentat](https://luisedmundo354.github.io/mentat_website/technology/#:~:text=3,retrieval%20and%20parsing%20later%20on)). Future iterations will integrate a relational database using **SQLAlchemy** with **SQLite** to manage patient records, enabling more robust queries and data management (while still keeping data offline).  
- **Planned C/C++ Optimizations:** To maximize performance on edge hardware, the team plans to implement critical components of the “language model miner” in C/C++ for optimized inference speed. These native modules (not yet included in the repository) will accelerate heavy computations and enable Mentat to run efficiently even on resource-constrained devices.  

## Installation  
Follow these steps to set up Mentat on your local machine:  

1. **Clone the Repository:** Obtain the source code from GitHub:  
   ```bash
   git clone https://github.com/luisedmundo354/mentat.git 
   cd mentat
   ```  

2. **Configure the Environment:** Ensure you have Python 3.8+ (or a compatible version) installed. It’s recommended to use a virtual environment or Conda environment for installation. For example, using Conda:  
   ```bash
   conda env create -f environment.yml  
   conda activate mentat  
   ```  
   This will install all required Python packages as specified in `environment.yml`. *(Alternatively, you can manually install dependencies via `pip` using the package list in the environment file.)*  

3. **Install the AI Model:** Mentat utilizes the Phi-3.5 mini model, which is not included in this repository due to its size. Download the model weights (approximately 2.8 GB) from the official source (e.g. the Hugging Face model repository for **Phi-3.5-mini**), and set up the LlamaEdge runtime as described in its documentation. Once downloaded, update the `config/settings.yaml` with the path to the model file or place the model in the default expected location. *(If the model is not installed, Mentat’s AI reasoning features will not be available.)*  

4. **Launch the Application:** After installing the dependencies and model, you can run Mentat:  
   ```bash
   python app.py
   ```  
   This command starts the Mentat GUI. You should see a window launch for the application interface.  

**Note:** Mentat is designed to run on systems with modest GPU capabilities. For the best experience, use a machine with a CUDA-compatible GPU or a device like the NVIDIA Jetson Orin for on-device inference. CPU-only operation is possible but may be slower for large language model inference.  

## Usage  
Once Mentat is installed and running, you can interact with it through its graphical interface. The software supports two primary workflows: (1) recording a new patient session, and (2) reviewing a patient’s data to get AI-assisted insights.  

- **Recording a New Patient Session:** To document a patient encounter or history, start a new session in the Mentat GUI (e.g., by clicking **“New Session”** or the equivalent option in the menu). Mentat will initiate a guided conversation, prompting the clinician or patient with relevant questions in sequence. The built-in language model uses proactive templates to drive this dialogue – it can rephrase questions and parse the answers on the fly to extract key information ([Technology | Mentat](https://luisedmundo354.github.io/mentat_website/technology/#:~:text=,information%20is%20gathered%E2%80%94the%20conversation%20concludes)). The Q&A continues until all necessary information has been gathered (Mentat checks for a stopping criterion indicating the data is sufficient). Once the interview is complete, the captured text is internally organized into structured categories (such as symptoms, history, medications, etc.) and saved as a JSON record for that patient ([Technology | Mentat](https://luisedmundo354.github.io/mentat_website/technology/#:~:text=3,retrieval%20and%20parsing%20later%20on)). The result is an efficient, error-minimized record of the patient’s information created with minimal manual typing.  

- **Reviewing Data & AI Insights:** For an existing patient, you can load their record via the UI (for example, by selecting the patient’s name or ID from a list of saved sessions). Mentat will retrieve the patient’s stored data and prepare an AI-generated summary or preliminary analysis. Under the hood, the system feeds the structured patient data into the local language model to generate a draft assessment or report ([Technology | Mentat](https://luisedmundo354.github.io/mentat_website/technology/#:~:text=1.%20Structured%20Data%20Retrieval%20,Augmented%20Generation%20%28RAG)). It then performs a retrieval-augmented generation (RAG) step: Mentat’s engine will query a local medical knowledge base or corpus for references (e.g. clinical guidelines or similar cases) and integrate those findings with the patient’s data ([Technology | Mentat](https://luisedmundo354.github.io/mentat_website/technology/#:~:text=,common%20treatments%2C%20or%20cautionary%20notes)). This combined output is presented as a context-aware summary of potential issues, recommendations, or next steps. For example, Mentat might highlight patterns in the symptoms that suggest certain conditions, remind the clinician of relevant medical literature, or suggest follow-up questions. All of this happens instantaneously within the app, and the clinician can review the AI’s suggestions alongside the original recorded data.  

Throughout the usage of Mentat, **all processing is done locally** – queries to the language model and knowledge retrieval do not require an internet connection. This means response times depend on your hardware but typically are optimized for real-time interaction. Moreover, because data never leaves the device, you maintain full control over sensitive patient information at all times. *(Remember that Mentat’s outputs are advisory and should be verified by a medical professional before taking action.)*  

## Features  
Mentat offers several key features and capabilities:  

- **Efficient Data Recording:** Automates the recording of patient symptoms and history through a conversational interface, minimizing manual data entry and reducing transcription errors ([Home | Mentat](https://luisedmundo354.github.io/mentat_website/#:~:text=1.%20Efficient%20Data%20Recording%20,Assisted%20Diagnostics)). Instead of writing notes from scratch, clinicians can rely on Mentat to capture structured information from natural dialogue.  
- **AI-Assisted Diagnostics:** Leverages a local **Phi-3.5 mini** LLM on LlamaEdge to provide reasoning and suggestions ([Home | Mentat](https://luisedmundo354.github.io/mentat_website/#:~:text=2.%20AI,aware%20insights)). The system uses retrieval-augmented generation (RAG) to incorporate relevant medical context, so its diagnostic insights are informed by both the patient’s data and up-to-date medical knowledge ([Home | Mentat](https://luisedmundo354.github.io/mentat_website/#:~:text=2.%20AI,aware%20insights)).  
- **Secure & Offline Operation:** Runs entirely offline with no reliance on external servers ([Home | Mentat](https://luisedmundo354.github.io/mentat_website/#:~:text=insights,ensures%20privacy%20and%20data%20integrity)). All data and computations stay within the clinic’s network or device, ensuring patient records remain private. Integration of a local database means data integrity and security are maintained without cloud services ([Home | Mentat](https://luisedmundo354.github.io/mentat_website/#:~:text=insights,ensures%20privacy%20and%20data%20integrity)).  
- **Easy Integration:** Designed for quick adoption into existing workflows and Healthcare Management Systems (HMS) ([Home | Mentat](https://luisedmundo354.github.io/mentat_website/#:~:text=4.%20Easy%20Integration%20,between%20nurses%2C%20doctors%2C%20and%20specialists)). Mentat’s modular architecture (with clearly separated UI, services, and data layers) makes it straightforward to interface with other hospital software. By bridging communication between nurses, doctors, and specialists through a unified platform, it facilitates smoother hand-offs and collaboration ([Home | Mentat](https://luisedmundo354.github.io/mentat_website/#:~:text=4.%20Easy%20Integration%20,between%20nurses%2C%20doctors%2C%20and%20specialists)).  

These features make Mentat a comprehensive tool for enhancing medical decision-making processes while fitting seamlessly into the clinical environment. As an evolving project, additional features like voice input, advanced analytics, and broader knowledge integration are on the roadmap.  

## License  
This project is licensed under the **MIT License**. Feel free to use, modify, and distribute the code in accordance with the license terms. See the [`LICENSE`](./LICENSE) file for details. *(All contributions to the repository are assumed to be under the same license to keep the project open and accessible.)*  

## Contributing  
Contributions to Mentat are welcome and appreciated! If you’d like to report a bug, request a feature, or contribute code:  

- **Issues:** Please open a GitHub Issue to report problems or suggest enhancements. Provide as much detail as possible, including steps to reproduce bugs or a clear description of the proposed feature.  
- **Pull Requests:** We accept pull requests on GitHub. If you plan to contribute a significant change, it’s a good idea to discuss it first by opening an issue or reaching out to the maintainers. Ensure that your code follows the project’s coding style and includes appropriate documentation or comments.  
- **Development Setup:** For development, install the required packages as described above. We encourage writing tests for new features or fixes when possible. Before submitting a pull request, run any existing tests or example scenarios to confirm that nothing is broken.  

By participating in this project, you help build a tool that could improve healthcare workflows and patient outcomes. We strive to foster an open and collaborative community. **Thank you for your interest in Mentat AI**, and we look forward to your contributions!