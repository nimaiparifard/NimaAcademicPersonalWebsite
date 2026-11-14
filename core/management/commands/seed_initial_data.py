"""Fill the site with everything that is already in your resume folder.

    python manage.py seed_initial_data

Safe to run again: rows are matched by slug/title and updated, not duplicated.
Edit the dictionaries below to change the starting content, or just edit it in
/admin afterwards.
"""
from datetime import date
from pathlib import Path

from django.core.files import File
from django.core.management.base import BaseCommand

from core.models import Award, Education, Experience, NewsItem, SiteProfile, SkillGroup
from learning.models import Book, Course  # noqa: F401  (left empty on purpose)
from portfolio.models import Project
from research.models import Publication

DEFAULT_SRC = Path(r"C:\Users\Nima\Desktop\english resumve")

PROFILE = dict(
    name="Nima Parifard",
    headline="NLP & Graph Learning Researcher · LLMs · GNNs · ML Engineering",
    availability="Open to fully funded PhD positions in Europe",
    short_bio=(
        "M.Sc. in Artificial Intelligence from Amirkabir University of Technology. I work on large language "
        "models and graph neural networks, in particular text-attributed graphs, and I build the engineering "
        "around them: RAG systems, agents, MLOps and production backends."
    ),
    long_bio=(
        "My research over the past three years has focused on Large Language Models (LLMs), Graph Neural Networks "
        "(GNNs) and complex networks, particularly text-attributed graphs, where every node carries a text "
        "description.\n\n"
        "In my recent work I developed DIVERGE, a framework that uses different LoRA initialization strategies to "
        "obtain diverse representations from language models and combines graph neural network predictions through "
        "a learnable ensemble. In a follow-up preprint, MAD-E, I study multi-axis diversity for ensembles of "
        "LLM-based graph encoders.\n\n"
        "I have also explored LLM compression (pruning, distillation, quantization), interpretability, "
        "Retrieval-Augmented Generation including GraphRAG, and multi-agent systems. On the engineering side I "
        "spent two years as a backend and DevOps engineer, and I build end-to-end ML platforms with MLflow, DVC, "
        "Airflow, FastAPI and Kubernetes.\n\n"
        "This site collects my research, projects, and what I am currently reading and learning."
    ),
    research_interests=(
        "Text-attributed graphs\nLLMs for graph learning\nEnsemble diversity\nLLM compression & interpretability\n"
        "Retrieval-Augmented Generation & GraphRAG\nMulti-agent systems\nMLOps"
    ),
    email="paryfardnim@gmail.com",
    location="Tehran, Iran",
    github="https://github.com/nimaiparifard",
    linkedin="https://www.linkedin.com/in/nima-parifard-6a454b1a8",
)

EXPERIENCE = [
    dict(kind="research", title="Researcher, NLP Lab", organization="Amirkabir University of Technology",
         location="Tehran", period="2022 – 2025", order=1, description="""\
Investigated representation learning for text-attributed graphs using LLMs and GNNs.
Developed DIVERGE: diverse LoRA initializations + a learnable GNN ensemble. State-of-the-art node classification on 6 of 7 benchmarks (Cora 89.9%, CiteSeer 79.5%, PubMed 95.3%, OGBN-ArXiv 78.1%) and best Macro-F1 on all 7, with no external LLM API calls.
Studied LLM compression (pruning, distillation, quantization) and neuron-level interpretability.
Built RAG pipelines with hybrid BM25 + dense retrieval, cross-encoder reranking, chunking strategies and GraphRAG.
Contributed to an industry research project on knowledge-graph extraction with LLMs."""),
    dict(kind="work", title="LLM Researcher", organization="PartAI", location="Tehran", period="2024 – 2025", order=2,
         description="""\
Surveyed and re-implemented state-of-the-art LLM papers on RAG, explainability and model compression, assessing real-world applicability.
Built evaluation and benchmarking pipelines on Persian datasets to validate re-implementations against reported results.
Applied interpretability methods (neuron-level analysis, attention visualization) to study LLM behavior."""),
    dict(kind="work", title="Backend & DevOps Engineer", organization="Arsh", location="Tehran", period="2020 – 2022",
         order=3, description="""\
Developed and maintained scalable backend systems and REST APIs with Django and Flask.
Migrated Simap, a large production platform, from Django 2 to Django 3.
Containerized services with Docker, automated builds with GitLab CI/CD, managed Linux deployments.
Maintained production systems backed by PostgreSQL and Redis."""),
    dict(kind="teaching", title="Teaching Assistant – Natural Language Processing", organization="Amirkabir University of Technology",
         period="2024", order=10, description="Designed three assignments from classical NLP methods to Transformer-based models."),
    dict(kind="teaching", title="Teaching Assistant – Deep Learning", organization="Amirkabir University of Technology",
         period="2023 – 2024", order=11, description="Designed eight assignments covering a range of deep learning topics."),
    dict(kind="teaching", title="Teaching Assistant – Pattern Recognition", organization="Amirkabir University of Technology",
         period="2023", order=12, description="""\
Designed five assignments combining conceptual questions, analytical problems and programming.
Designed a final programming project integrating the course concepts."""),
]

EDUCATION = [
    dict(degree="M.Sc., Artificial Intelligence", institution="Amirkabir University of Technology", location="Tehran, Iran",
         period="2023 – 2026", gpa="19.07 / 20", supervisor="Dr. Saeedeh Momtazi",
         thesis="Improving Text-Attributed Graph Performance with Large Language Models", order=1,
         notes="Coursework: Pattern Recognition, Linear Algebra, Convex Optimization, Statistical Machine Learning"),
    dict(degree="B.Sc., Software Engineering", institution="Kharazmi University", location="Tehran, Iran",
         period="2018 – 2023", gpa="15.08 / 20", order=2),
]

SKILLS = [
    ("ML & NLP", "Python, PyTorch, PyTorch Geometric, Hugging Face Transformers, PEFT (LoRA), SciPy, scikit-learn, LightGBM"),
    ("LLM systems", "RAG, GraphRAG, hybrid retrieval & reranking, LlamaIndex, LangChain, LangGraph, FAISS, pgvector, Neo4j, vLLM, Ollama, MCP"),
    ("MLOps", "MLflow, DVC, Airflow, Feast, Prometheus, Grafana, GitHub Actions, GitLab CI"),
    ("Engineering", "Django, Django REST Framework, FastAPI, Celery, PostgreSQL, Redis, Docker, Kubernetes, Helm, Linux"),
]

AWARDS = [
    ("Ranked 4th in the national M.Sc. entrance examination", "Iran National Organization of Educational Testing (Sanjesh)", ""),
    ("Ranked 2nd academically in my M.Sc. cohort", "Amirkabir University of Technology", ""),
    ("M.Sc. thesis selected as an Outstanding Research Project", "Iran National Science Foundation (INSF)", ""),
]

PUBLICATIONS = [
    dict(title="DIVERGE: Diverse Initializations for Vector Ensembles in Representation-aware Text-Attributed Graph Encoding with Large Language Models",
         authors="Parifard, N., Momtazi, S.", venue="Information Processing & Management", year="2026",
         status="review", featured=True, order=1,
         notes="Revised manuscript under review.",
         abstract=("DIVERGE uses different LoRA initialization strategies to obtain diverse representations from a language "
                   "model and combines GNN predictions through a learnable ensemble. It reaches state-of-the-art node "
                   "classification accuracy on six of seven benchmarks and the best Macro-F1 on all seven, without any external LLM API calls."),
         code_url="https://github.com/nimaiparifard/DIVERGE_implementation"),
    dict(title="MAD-E: Multi-Axis Diversity for Ensembles of LLM-based Graph Encoders on Text-Attributed Graphs",
         authors="Parifard, N., Momtazi, S.", venue="Preprint", year="2026", status="preprint", featured=True, order=2,
         abstract=("Ensembles of language-model-based encoders can improve node classification on text-attributed graphs, but it is "
                   "unclear which sources of diversity make an ensemble better. MAD-E is a library of ensemble members built from the "
                   "same cached LoRA embeddings that differ in one component only, across six axes of diversity.")),
]

PROJECTS = [
    dict(title="RiskLens — Credit Risk & Fraud Scoring Platform", slug="risklens", category="MLOps", year="2026", featured=True, order=1,
         status="done", summary="End-to-end credit-risk and fraud scoring with calibrated ensembles, SHAP reason codes and automated retraining.",
         tech="LightGBM, XGBoost, CatBoost, SHAP, MLflow, DVC, FastAPI, Django, Celery, React, TypeScript, Docker, GitHub Actions, Prometheus, Grafana",
         metrics="Credit ROC-AUC: 0.793\nFraud ROC-AUC: 0.906\nFraud recall @1% FPR: 47.8%\nProjected loss cut: 23%\nFraud p95 latency: 18 ms",
         description=("An end-to-end credit-risk and fraud scoring platform built on Home Credit (307K loans) and IEEE-CIS (590K transactions). "
                      "A calibrated LightGBM/XGBoost/CatBoost stacking ensemble drives the credit model; a separate model scores fraud."),
         highlights="""\
Decision thresholds chosen by expected business cost: 23% lower projected credit losses than approve-all, at an 86% approval rate.
SHAP reason codes, A–E risk grades and fairness gates.
Automated retraining with DVC and an MLflow champion/challenger workflow in GitHub Actions (cost, fairness and manual-approval gates), plus nightly PSI drift monitoring.
Models served with FastAPI at 18 ms p95 (fraud) and 95 ms p95 (credit + SHAP) behind a Django/React officer dashboard, monitored with Prometheus and Grafana."""),
    dict(title="DemandOps — MLOps Platform for Retail Demand Forecasting", slug="demandops", category="MLOps", year="2026", featured=True, order=2,
         status="done", summary="MLOps-first platform producing 28-day forecasts for the 30,490 item-store series of M5 (Walmart).",
         tech="Python, LightGBM, Airflow, MLflow, DVC, Feast, FastAPI, Streamlit, Kubernetes, Helm, Argo CD, Prometheus, Grafana, Docker, GitHub Actions",
         metrics="WRMSSE: 0.656\nSeasonal naive: 0.909\nAutoETS: 0.752\nServing p95: 6–8 ms\nTests: 98 @ 93% coverage",
         description=("A global LightGBM model reaches 0.656 WRMSSE versus 0.909 for seasonal naive and 0.752 for AutoETS in a 3-fold rolling-origin "
                      "backtest on a 3,000-series sample. All 853,720 forecast rows for every series are generated in 6 seconds."),
         highlights="""\
Four Airflow DAGs orchestrate daily ingest, training, promotion gates and batch forecasting, with MLflow model registry, Feast offline/online features and PostgreSQL.
PSI drift alerts in Prometheus trigger automatic retraining.
FastAPI serving at 6–8 ms p95 (50–120 req/s per worker), a Streamlit forecast viewer and a what-if price tool.
Helm, Argo CD and Argo Rollouts (GitOps canary with auto-rollback) manifests and OpenTofu/Ansible deployments for Kubernetes (k3d/k3s). The cluster-side canary path is written but not yet run on a cluster."""),
    dict(title="FinSight — RAG for SEC Filings", slug="finsight", category="LLM", year="2026", featured=True, order=3, status="done",
         summary="Question answering over 10-K / 10-Q filings with page-level citations, table support and a CI evaluation gate.",
         tech="Python, LlamaIndex, LangGraph, sentence-transformers, pgvector, FastAPI, Django, Celery, React, TypeScript, MLflow, Langfuse, Prometheus, Docker Compose",
         metrics="Tests: 85\nEval sets: 3\nCI gate: >3-pt regression",
         description=("A RAG system that answers questions over SEC filings with page-level citations, including table data. It combines hybrid "
                      "retrieval (dense + BM25/Postgres full-text), optional reranking, query transformations (multi-query, HyDE, decomposition) "
                      "and section-aware chunking with contextual headers."),
         highlights="""\
Reduces hallucination risk: arithmetic is done by a calculator instead of the LLM, cited numbers are verified against retrieved text, and the system refuses to answer when evidence is missing.
Modular finsight package behind swappable, YAML-configured interfaces, served through FastAPI, Django/Celery and a React frontend.
Evaluation harness (FinanceBench, FinQA, TAT-QA; Recall@k, MRR, nDCG, faithfulness) with a CI gate that fails PRs on a >3-point metric regression.
85 tests run without GPU or network."""),
    dict(title="DIVERGE — LLM-based Graph Encoders", slug="diverge", category="Graph ML", year="2026", featured=False, order=4, status="research",
         summary="Research code for diverse LoRA initializations combined through a learnable GNN ensemble on text-attributed graphs.",
         tech="PyTorch, PyTorch Geometric, Hugging Face, PEFT (LoRA)", repo_url="https://github.com/nimaiparifard/DIVERGE_implementation",
         metrics="Cora: 89.9%\nCiteSeer: 79.5%\nPubMed: 95.3%\nOGBN-ArXiv: 78.1%",
         description="Reference implementation accompanying the DIVERGE paper (under review). Beats TAPE by 0.3–2.2 points without any external LLM API calls."),
    dict(title="Knowledge Graph Extraction & GraphRAG for Enterprise Documents", slug="kg-graphrag", category="LLM", year="2025", order=5, status="done",
         summary="Fully automatic pipeline that builds a knowledge graph from internal documents and answers complex questions with GraphRAG.",
         tech="LLMs, Neo4j, GraphRAG",
         description=("An ontology (the entities and relations that matter in the documents) is induced automatically; each document then goes "
                      "through a four-stage pipeline: entity recognition, relation extraction, coreference resolution and entity linking. "
                      "The resulting graph is loaded into Neo4j and queried with GraphRAG at question time.")),
    dict(title="FinWise Course Bot — Hybrid-RAG Assistant", slug="finwise-bot", category="LLM", year="2025", order=6, status="done",
         summary="Persian/English course-support assistant for Telegram and web that answers strictly from stored data and escalates to staff.",
         tech="Python, Django, MongoDB, LlamaIndex, BM25, OpenAI, Claude, Telegram Bot API, Docker Compose",
         highlights="""\
Hybrid retrieval (BM25 + vector with rank fusion, BM25 fallback) in LlamaIndex.
Structured LLM output (can_answer, answer, reason) escalates unanswerable questions to staff, who reply from Telegram or the Django admin and can save answers to the FAQ.
Crawler syncs course data into MongoDB with admin edit locks so manual changes are never overwritten; test suite uses mocked Telegram, LLM and embedding services.""",
         description="Supports OpenAI-compatible and Anthropic Claude models."),
    dict(title="Multi-Agent E-commerce Shopping Assistant", slug="shopping-assistant", category="LLM", year="2025", order=7, status="done",
         summary="A router sends each request to specialized agents: product exploration, details, comparison, shop & price, image-based search.",
         tech="LangChain, FastAPI, FAISS, OpenAI, Python", description="Grounded answers come from FAISS semantic search over a product database."),
    dict(title="Stock MCP Bot — LLM Agent for Market Analysis", slug="stock-mcp-bot", category="LLM", year="2025", order=8, status="done",
         summary="LLM chatbot that orchestrates tools through the Model Context Protocol for real-time Yahoo Finance data and technical analysis.",
         tech="Python, FastAPI, MCP, OpenAI GPT, Docker",
         description="Computes RSI, moving averages and volatility. Shipped as a Dockerized FastAPI service with conversation memory and structured logging."),
]

NEWS = [
    dict(slug="mad-e-preprint", date=date(2026, 11, 3), title="MAD-E preprint is ready",
         summary="Our study of multi-axis diversity for ensembles of LLM-based graph encoders is now a preprint.",
         body="MAD-E: Multi-Axis Diversity for Ensembles of LLM-based Graph Encoders on Text-Attributed Graphs, with Saeedeh Momtazi.", pinned=False),
    dict(slug="website-launch", date=date(2026, 11, 14), title="Website launched",
         summary="Projects, research, reading and courses in one place. I will keep adding to it.",
         body="This site collects my research, projects, books and courses. News and new projects will appear here as they happen.", pinned=True),
]


class Command(BaseCommand):
    help = "Load your resume data into the site (idempotent)."

    def add_arguments(self, parser):
        parser.add_argument("--src", default=str(DEFAULT_SRC), help="Folder with photo and CV files")

    def handle(self, *args, **opts):
        src = Path(opts["src"])

        profile = SiteProfile.get() or SiteProfile()
        for k, v in PROFILE.items():
            setattr(profile, k, v)
        photo, cv = src / "nima photo.jpg", src / "academic_resume" / "nima_parifard_academic_cv.pdf"
        if photo.exists() and not profile.photo:
            with photo.open("rb") as fh:
                profile.photo.save("nima.jpg", File(fh), save=False)
        if cv.exists() and not profile.cv_file:
            with cv.open("rb") as fh:
                profile.cv_file.save("Nima_Parifard_CV.pdf", File(fh), save=False)
        profile.save()

        for e in EXPERIENCE:
            Experience.objects.update_or_create(title=e["title"], organization=e["organization"], defaults=e)
        for e in EDUCATION:
            Education.objects.update_or_create(degree=e["degree"], institution=e["institution"], defaults=e)
        for i, (name, skills) in enumerate(SKILLS, 1):
            SkillGroup.objects.update_or_create(name=name, defaults=dict(skills=skills, order=i))
        for i, (title, issuer, year) in enumerate(AWARDS, 1):
            Award.objects.update_or_create(title=title, defaults=dict(issuer=issuer, year=year, order=i))
        for p in PUBLICATIONS:
            Publication.objects.update_or_create(title=p["title"], defaults=p)
        for p in PROJECTS:
            Project.objects.update_or_create(slug=p["slug"], defaults=p)
        for n in NEWS:
            NewsItem.objects.update_or_create(slug=n["slug"], defaults=n)

        self.stdout.write(self.style.SUCCESS("Seeded profile, CV, projects, publications and news."))
