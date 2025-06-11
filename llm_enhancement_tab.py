"""
LLM Enhancement Testing Tab for GUARDIAN
Tests and demonstrates integration with free LLM services for AI/Quantum knowledge enhancement
"""

import streamlit as st
import asyncio
import json
from utils.free_llm_services import free_llm_manager
from utils.llm_intelligence_enhancer import llm_enhancer
from utils.knowledge_base_integrator import knowledge_integrator

def render():
    """Render the LLM Enhancement tab"""
    
    # Enhanced header matching Cyber Institute style
    st.markdown(
        """<div style="background: linear-gradient(135deg, #082454 0%, #10244D 50%, #133169 100%); padding: 2.5rem; border-radius: 12px; margin-bottom: 2rem; color: white;">
            <h1 style="color: white; margin-bottom: 1.2rem; font-size: 2.2rem; font-weight: 700; text-align: center;">
                GUARDIAN LLM Intelligence Enhancement
            </h1>
            <div style="background: rgba(255,255,255,0.1); padding: 1.5rem; border-radius: 10px; margin: 1.5rem 0; border: 1px solid rgba(255,255,255,0.2);">
                <h3 style="color: #3D9BE9; margin-bottom: 1rem; font-size: 1.4rem; font-weight: 600; text-align: center;">
                    Multi-LLM Integration for Enhanced AI Ethics & Quantum Security Intelligence
                </h3>
                <p style="color: #e5e7eb; text-align: center; font-size: 1.1rem; line-height: 1.6; margin: 0;">
                    Connect GUARDIAN to free and open-source LLM services to enhance understanding of AI ethics norms, quantum security best practices, and cybersecurity frameworks before ingesting large policy document datasets.
                </p>
            </div>
        </div>""", 
        unsafe_allow_html=True
    )
    
    # Main tabs for different aspects of LLM enhancement
    tab1, tab2, tab3, tab4 = st.tabs([
        "Service Testing", 
        "Knowledge Integration", 
        "Data Architecture",
        "Enhancement Demo"
    ])
    
    with tab1:
        render_service_testing_tab()
    
    with tab2:
        render_knowledge_integration_tab()
    
    with tab3:
        render_data_architecture_tab()
    
    with tab4:
        render_enhancement_demo_tab()

def render_service_testing_tab():
    """Test available free LLM services"""
    
    st.markdown("### **Free LLM Service Testing**")
    st.markdown("Test which free LLM services are available and working for GUARDIAN enhancement")
    
    # Service recommendations based on use case
    col1, col2 = st.columns([1, 1])
    
    with col1:
        use_case = st.selectbox(
            "Select your primary use case:",
            ["ai_ethics", "quantum_security", "cybersecurity", "general"],
            format_func=lambda x: {
                "ai_ethics": "AI Ethics & Fairness",
                "quantum_security": "Quantum Security",
                "cybersecurity": "Cybersecurity Frameworks",
                "general": "General Enhancement"
            }[x]
        )
    
    with col2:
        if st.button("Get Recommendations", type="primary"):
            recommendations = free_llm_manager.get_service_recommendations(use_case)
            
            st.markdown("#### **Recommended Services for Your Use Case:**")
            for rec in recommendations:
                st.markdown(f"""
                **{rec['priority']}. {rec['service'].title()}**
                - {rec['reason']}
                """)
    
    st.markdown("---")
    
    # Test all services
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("Test All Services", type="secondary"):
            with st.spinner("Testing all free LLM services..."):
                try:
                    # Run async test
                    results = asyncio.run(free_llm_manager.test_all_services())
                    
                    st.success(f"Tested {results['total_tested']} services")
                    
                    # Available services
                    if results['available_services']:
                        st.markdown("#### **Available Services (Ready to Use):**")
                        for service in results['available_services']:
                            st.markdown(f"""
                            **{service['name'].title()}**
                            - Cost: {service['cost']}
                            - Specialization: {service['specialization']}
                            - Status: ✅ {service['status']}
                            """)
                    
                    # Services needing setup
                    if results['needs_setup']:
                        st.markdown("#### **Services Needing Setup:**")
                        for service in results['needs_setup']:
                            with st.expander(f"Setup {service['name'].title()}"):
                                st.markdown(f"**Cost:** {service['cost']}")
                                st.markdown(f"**Setup:** {service['setup_instructions']}")
                    
                    # Errors
                    if results['errors']:
                        st.markdown("#### **Services with Issues:**")
                        for error in results['errors']:
                            st.warning(f"{error['name']}: {error.get('error', 'Unknown error')}")
                
                except Exception as e:
                    st.error(f"Testing failed: {str(e)}")
    
    with col2:
        if st.button("Show Setup Instructions"):
            instructions = free_llm_manager.get_setup_instructions()
            
            st.markdown("#### **Complete Setup Instructions:**")
            for service, instruction in instructions.items():
                with st.expander(f"{service.title()} Setup"):
                    st.code(instruction.strip(), language="bash")
    
    # Individual service testing
    st.markdown("---")
    st.markdown("#### **Test Individual Services:**")
    
    service_options = [
        "ollama", "huggingface", "groq", "together_ai", 
        "perplexity", "cohere", "fireworks", "deepinfra"
    ]
    
    selected_service = st.selectbox("Select service to test:", service_options)
    
    if st.button(f"Test {selected_service.title()}", key=f"test_{selected_service}"):
        with st.spinner(f"Testing {selected_service}..."):
            try:
                result = asyncio.run(free_llm_manager.test_service_availability(selected_service))
                
                if result.get("status") == "available":
                    st.success(f"{selected_service.title()} is available!")
                    st.json(result)
                elif result.get("status") == "needs_key":
                    st.warning(f"{selected_service.title()} needs API key setup")
                    st.info(result.get("setup_instructions", "Check documentation"))
                else:
                    st.error(f"{selected_service.title()} test failed")
                    st.json(result)
            
            except Exception as e:
                st.error(f"Test failed: {str(e)}")

def render_knowledge_integration_tab():
    """Knowledge base integration interface"""
    
    st.markdown("### **External Knowledge Source Integration**")
    st.markdown("Connect to authoritative sources for AI ethics, quantum security, and cybersecurity knowledge")
    
    # Knowledge source status
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("Check Knowledge Sources", type="primary"):
            status = knowledge_integrator.get_sync_status()
            
            st.markdown("#### **Knowledge Source Status:**")
            st.metric("Total Sources", status['total_sources'])
            st.metric("Synced Sources", status['synced_sources'])
            st.metric("Total Documents", status['total_documents'])
            
            if status['cache_status']:
                st.markdown("#### **Cache Status:**")
                for source, cache_info in status['cache_status'].items():
                    st.markdown(f"**{source}:** {cache_info['count']} documents")
    
    with col2:
        domains = st.multiselect(
            "Select domains to sync:",
            ["ai_ethics", "quantum_security", "cybersecurity"],
            default=["ai_ethics", "quantum_security", "cybersecurity"]
        )
        
        if st.button("Sync Knowledge Sources"):
            with st.spinner("Synchronizing knowledge sources..."):
                try:
                    results = asyncio.run(knowledge_integrator.sync_knowledge_sources(domains))
                    
                    st.success(f"Retrieved {results['total_documents']} documents")
                    
                    if results['successful']:
                        st.markdown("#### **Successful Syncs:**")
                        for success in results['successful']:
                            st.markdown(f"- {success['source']}: {success['documents_retrieved']} docs")
                    
                    if results['failed']:
                        st.markdown("#### **Failed Syncs:**")
                        for failure in results['failed']:
                            st.warning(f"- {failure}")
                
                except Exception as e:
                    st.error(f"Sync failed: {str(e)}")
    
    st.markdown("---")
    
    # Knowledge search interface
    st.markdown("#### **Search Integrated Knowledge:**")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        search_query = st.text_input("Search knowledge base:", placeholder="e.g., AI fairness guidelines")
    
    with col2:
        search_domains = st.multiselect(
            "Filter by domain:",
            ["ai_ethics", "quantum_security", "cybersecurity"],
            key="search_domains"
        )
    
    if st.button("Search Knowledge") and search_query:
        with st.spinner("Searching..."):
            try:
                results = asyncio.run(knowledge_integrator.search_knowledge(
                    search_query, 
                    search_domains if search_domains else None
                ))
                
                if results:
                    st.markdown(f"#### **Found {len(results)} relevant documents:**")
                    
                    for i, doc in enumerate(results[:10]):  # Show top 10
                        with st.expander(f"{i+1}. {doc.get('title', 'Untitled')}"):
                            st.markdown(f"**Source:** {doc.get('source', 'Unknown')}")
                            st.markdown(f"**Domain:** {doc.get('knowledge_domain', 'General')}")
                            if 'description' in doc or 'abstract' in doc:
                                desc = doc.get('description', doc.get('abstract', ''))
                                st.markdown(f"**Summary:** {desc[:300]}...")
                            if 'relevance_score' in doc:
                                st.metric("Relevance Score", f"{doc['relevance_score']:.2f}")
                else:
                    st.info("No results found. Try different search terms or sync more sources.")
            
            except Exception as e:
                st.error(f"Search failed: {str(e)}")

def render_data_architecture_tab():
    """Data architecture strategy for LLM enhancement"""
    
    st.markdown("### **Data Architecture Strategy**")
    st.markdown("Recommended data storage and processing architecture for GUARDIAN's LLM enhancement")
    
    # Architecture recommendations
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### **Recommended Architecture:**")
        
        architecture_options = {
            "Hybrid PostgreSQL + Vector DB": {
                "description": "Current PostgreSQL for structured data + Chroma/FAISS for embeddings",
                "pros": ["Leverages existing DB", "Good for similarity search", "Cost effective"],
                "cons": ["Additional complexity", "Sync requirements"],
                "cost": "Low",
                "best_for": "Document similarity and recommendation systems"
            },
            "PostgreSQL with pgvector": {
                "description": "Single database with vector extension for embeddings",
                "pros": ["Single database", "ACID compliance", "Familiar SQL"],
                "cons": ["Extension dependency", "Scaling limitations"],
                "cost": "Very Low",
                "best_for": "Unified data model with moderate scale"
            },
            "Document-Oriented (MongoDB)": {
                "description": "Schema-flexible document storage with full-text search",
                "pros": ["Flexible schema", "Built-in search", "JSON-native"],
                "cons": ["Migration required", "Learning curve"],
                "cost": "Medium",
                "best_for": "Unstructured policy documents with varying schemas"
            },
            "Data Lake (MinIO + Pandas)": {
                "description": "Object storage with structured processing layers",
                "pros": ["Scalable storage", "Cost effective", "Multiple formats"],
                "cons": ["Processing complexity", "Consistency challenges"],
                "cost": "Low",
                "best_for": "Large-scale document ingestion and batch processing"
            }
        }
        
        selected_arch = st.selectbox(
            "Select architecture to explore:",
            list(architecture_options.keys())
        )
        
        arch_info = architecture_options[selected_arch]
        
        st.markdown(f"**{selected_arch}**")
        st.markdown(f"*{arch_info['description']}*")
        
        st.markdown("**Advantages:**")
        for pro in arch_info['pros']:
            st.markdown(f"- {pro}")
        
        st.markdown("**Considerations:**")
        for con in arch_info['cons']:
            st.markdown(f"- {con}")
        
        st.metric("Implementation Cost", arch_info['cost'])
        st.info(f"**Best for:** {arch_info['best_for']}")
    
    with col2:
        st.markdown("#### **Current GUARDIAN Architecture:**")
        
        current_architecture = {
            "Database": "PostgreSQL",
            "Document Storage": "Database BLOBs + File system",
            "Vector Search": "Not implemented",
            "LLM Integration": "OpenAI + Anthropic",
            "Knowledge Base": "Local document repository",
            "Caching": "In-memory Python dictionaries"
        }
        
        for component, implementation in current_architecture.items():
            st.markdown(f"**{component}:** {implementation}")
        
        st.markdown("---")
        
        st.markdown("#### **Enhancement Recommendations:**")
        
        enhancements = [
            "Add vector embeddings for document similarity",
            "Implement knowledge base caching with Redis",
            "Create document preprocessing pipeline",
            "Add multi-LLM routing and fallback",
            "Implement incremental learning from new documents",
            "Add real-time knowledge source synchronization"
        ]
        
        for enhancement in enhancements:
            st.markdown(f"- {enhancement}")
    
    st.markdown("---")
    
    # Implementation guidance
    st.markdown("#### **Implementation Phases:**")
    
    phases = {
        "Phase 1: Vector Enhancement": {
            "duration": "1-2 weeks",
            "tasks": [
                "Add document embedding generation",
                "Implement similarity search",
                "Enhance recommendation engine"
            ],
            "dependencies": ["sentence-transformers", "chromadb or faiss"]
        },
        "Phase 2: Multi-LLM Integration": {
            "duration": "2-3 weeks", 
            "tasks": [
                "Integrate free LLM services",
                "Implement fallback routing",
                "Add domain-specific prompting"
            ],
            "dependencies": ["API keys for services", "async request handling"]
        },
        "Phase 3: Knowledge Base Expansion": {
            "duration": "3-4 weeks",
            "tasks": [
                "Connect external knowledge sources",
                "Implement automated synchronization",
                "Add knowledge validation and scoring"
            ],
            "dependencies": ["External API access", "Data validation frameworks"]
        }
    }
    
    for phase, details in phases.items():
        with st.expander(phase):
            st.markdown(f"**Duration:** {details['duration']}")
            st.markdown("**Tasks:**")
            for task in details['tasks']:
                st.markdown(f"- {task}")
            st.markdown("**Dependencies:**")
            for dep in details['dependencies']:
                st.markdown(f"- {dep}")

def render_enhancement_demo_tab():
    """Demonstrate LLM enhancement capabilities"""
    
    st.markdown("### **LLM Enhancement Demonstration**")
    st.markdown("Test enhanced document analysis using multiple LLM sources")
    
    # Sample text for testing
    sample_texts = {
        "AI Ethics Policy": """
        This document establishes principles for responsible AI development including fairness, 
        transparency, accountability, and human oversight. Organizations must implement bias 
        testing, explainable AI mechanisms, and regular audits of AI systems impacting human decisions.
        """,
        "Quantum Security Framework": """
        Post-quantum cryptography transition requires assessment of current cryptographic 
        implementations, timeline for quantum computer threats, and migration strategy for 
        quantum-resistant algorithms including lattice-based and hash-based cryptography.
        """,
        "Cybersecurity Standard": """
        This framework defines security controls for critical infrastructure including 
        identity management, access controls, continuous monitoring, incident response, 
        and supply chain risk management aligned with NIST Cybersecurity Framework.
        """
    }
    
    # Text selection
    col1, col2 = st.columns([1, 1])
    
    with col1:
        selected_sample = st.selectbox(
            "Select sample text or enter your own:",
            ["Custom Text"] + list(sample_texts.keys())
        )
        
        if selected_sample == "Custom Text":
            test_text = st.text_area(
                "Enter text to analyze:",
                height=150,
                placeholder="Paste AI ethics, quantum security, or cybersecurity content..."
            )
        else:
            test_text = sample_texts[selected_sample]
            st.text_area(
                "Sample text:",
                value=test_text,
                height=150,
                disabled=True
            )
    
    with col2:
        analysis_domain = st.selectbox(
            "Analysis domain:",
            ["ai_ethics", "quantum_security", "cybersecurity"],
            format_func=lambda x: {
                "ai_ethics": "AI Ethics & Fairness",
                "quantum_security": "Quantum Security",
                "cybersecurity": "Cybersecurity"
            }[x]
        )
        
        include_knowledge = st.checkbox(
            "Include external knowledge enhancement",
            value=True,
            help="Use external knowledge sources for enhanced analysis"
        )
        
        if st.button("Analyze with Enhanced LLM", type="primary") and test_text:
            with st.spinner("Running enhanced analysis..."):
                try:
                    # Run enhanced analysis
                    enhanced_result = asyncio.run(
                        llm_enhancer.enhance_document_analysis(test_text, analysis_domain)
                    )
                    
                    st.success("Enhanced analysis complete!")
                    
                    # Display results
                    col1, col2 = st.columns([1, 1])
                    
                    with col1:
                        st.markdown("#### **Primary Analysis:**")
                        if 'primary_analysis' in enhanced_result:
                            primary = enhanced_result['primary_analysis']
                            if isinstance(primary, dict):
                                st.json(primary)
                            else:
                                st.markdown(str(primary))
                        
                        if 'confidence_score' in enhanced_result:
                            st.metric(
                                "Confidence Score", 
                                f"{enhanced_result['confidence_score']:.2f}"
                            )
                    
                    with col2:
                        st.markdown("#### **Supporting Insights:**")
                        if 'supporting_insights' in enhanced_result:
                            insights = enhanced_result['supporting_insights']
                            for i, insight in enumerate(insights):
                                with st.expander(f"Source {i+1}: {insight.get('source', 'Unknown')}"):
                                    st.markdown(f"**Domain:** {insight.get('domain', 'General')}")
                                    if 'analysis' in insight:
                                        analysis = insight['analysis']
                                        if isinstance(analysis, str):
                                            st.markdown(analysis[:500] + "..." if len(analysis) > 500 else analysis)
                                        else:
                                            st.json(analysis)
                        
                        if 'knowledge_sources_used' in enhanced_result:
                            sources = enhanced_result['knowledge_sources_used']
                            st.markdown("**Knowledge Sources Used:**")
                            for source in sources:
                                if source:
                                    st.markdown(f"- {source}")
                    
                    # Enhanced metadata
                    if 'enhanced_metadata' in enhanced_result:
                        st.markdown("#### **Enhanced Scoring:**")
                        metadata = enhanced_result['enhanced_metadata']
                        
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            if 'ai_ethics_score' in metadata:
                                st.metric("AI Ethics", f"{metadata['ai_ethics_score']}/100")
                        
                        with col2:
                            if 'quantum_security_score' in metadata:
                                st.metric("Quantum Security", f"{metadata['quantum_security_score']}/100")
                        
                        with col3:
                            if 'cybersecurity_score' in metadata:
                                st.metric("Cybersecurity", f"{metadata['cybersecurity_score']}/100")
                
                except Exception as e:
                    st.error(f"Analysis failed: {str(e)}")
                    st.info("This may indicate that LLM services need setup or API keys are missing.")
    
    st.markdown("---")
    
    # Comparison with standard analysis
    st.markdown("#### **Compare Enhancement Results:**")
    
    if st.button("Compare Standard vs Enhanced Analysis") and test_text:
        with st.spinner("Running comparison..."):
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("**Standard GUARDIAN Analysis:**")
                # Use existing document analyzer
                from utils.document_analyzer import analyze_document_metadata
                standard_result = analyze_document_metadata(test_text, "sample_document")
                st.json(standard_result)
            
            with col2:
                st.markdown("**Enhanced Multi-LLM Analysis:**")
                try:
                    enhanced_result = asyncio.run(
                        llm_enhancer.enhance_document_analysis(test_text, analysis_domain)
                    )
                    
                    # Show simplified comparison
                    comparison = {
                        "confidence_score": enhanced_result.get('confidence_score', 0),
                        "knowledge_sources": len(enhanced_result.get('knowledge_sources_used', [])),
                        "enhanced_scores": enhanced_result.get('enhanced_metadata', {}),
                        "insights_count": len(enhanced_result.get('supporting_insights', []))
                    }
                    st.json(comparison)
                
                except Exception as e:
                    st.error(f"Enhanced analysis failed: {str(e)}")