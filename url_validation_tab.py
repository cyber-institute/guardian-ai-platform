"""
URL Validation Management Tab
Comprehensive interface for validating and managing document URLs
"""

import streamlit as st
import psycopg2
import os
from utils.url_validator import URLValidator, validate_single_url
import pandas as pd
from datetime import datetime

def render():
    """Render the URL validation management interface"""
    st.title("🔗 URL Validation Management")
    
    # Get database connection
    try:
        conn = psycopg2.connect(os.environ.get('DATABASE_URL'))
        cursor = conn.cursor()
    except Exception as e:
        st.error(f"Database connection failed: {e}")
        return
    
    # URL Status Summary
    st.subheader("📊 URL Status Overview")
    
    try:
        cursor.execute("""
            SELECT 
                COUNT(*) as total_urls,
                SUM(CASE WHEN url_valid = true THEN 1 ELSE 0 END) as valid_urls,
                SUM(CASE WHEN url_valid = false THEN 1 ELSE 0 END) as invalid_urls,
                SUM(CASE WHEN url_valid IS NULL THEN 1 ELSE 0 END) as unverified_urls
            FROM documents 
            WHERE source IS NOT NULL AND source != '' AND source LIKE 'http%'
        """)
        
        stats = cursor.fetchone()
        
        if stats and stats[0] > 0:
            total, valid, invalid, unverified = stats
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total URLs", total)
            with col2:
                st.metric("Valid URLs", valid, delta=f"{(valid/total*100):.1f}%")
            with col3:
                st.metric("Invalid URLs", invalid, delta=f"{(invalid/total*100):.1f}%")
            with col4:
                st.metric("Unverified URLs", unverified, delta=f"{(unverified/total*100):.1f}%")
        else:
            st.info("No URLs found in database")
            
    except Exception as e:
        st.error(f"Error getting URL statistics: {e}")
    
    # Validation Controls
    st.subheader("🔧 Validation Controls")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔍 Validate All URLs", type="primary"):
            validate_all_urls_interface(cursor, conn)
    
    with col2:
        if st.button("🔄 Re-validate Failed URLs"):
            revalidate_failed_urls(cursor, conn)
    
    with col3:
        if st.button("🧹 Clear Validation Data"):
            clear_validation_data(cursor, conn)
    
    # Manual URL Testing
    st.subheader("🧪 Manual URL Testing")
    
    test_url = st.text_input("Enter URL to test:", placeholder="https://example.com/document.pdf")
    
    if st.button("Test URL") and test_url:
        with st.spinner("Testing URL..."):
            is_valid, status = validate_single_url(test_url)
            
            if is_valid:
                st.success(f"✅ URL is valid: {status}")
            else:
                st.error(f"❌ URL is invalid: {status}")
    
    # Detailed URL Status Table
    st.subheader("📋 Detailed URL Status")
    
    try:
        cursor.execute("""
            SELECT 
                id,
                title,
                source,
                url_valid,
                url_status,
                url_checked,
                source_redirect
            FROM documents 
            WHERE source IS NOT NULL AND source != '' AND source LIKE 'http%'
            ORDER BY url_checked DESC, title
        """)
        
        url_data = cursor.fetchall()
        
        if url_data:
            # Create DataFrame for display
            df_data = []
            for row in url_data:
                doc_id, title, source, valid, status, checked, redirect = row
                
                # Format status
                if valid is True:
                    status_icon = "✅"
                    status_color = "green"
                elif valid is False:
                    status_icon = "❌"
                    status_color = "red"
                else:
                    status_icon = "⚠️"
                    status_color = "orange"
                
                df_data.append({
                    'ID': doc_id,
                    'Title': title[:50] + '...' if len(title) > 50 else title,
                    'URL': source[:60] + '...' if len(source) > 60 else source,
                    'Status': f"{status_icon} {status or 'Not checked'}",
                    'Checked': checked.strftime('%Y-%m-%d %H:%M') if checked else 'Never',
                    'Redirect': redirect[:50] + '...' if redirect and len(redirect) > 50 else (redirect or 'None')
                })
            
            df = pd.DataFrame(df_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Individual URL actions
            st.subheader("🔧 Individual URL Actions")
            
            selected_doc = st.selectbox(
                "Select document to manage:",
                options=[(row[0], row[1]) for row in url_data],
                format_func=lambda x: f"{x[1][:60]}{'...' if len(x[1]) > 60 else ''}"
            )
            
            if selected_doc:
                doc_id, doc_title = selected_doc
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button(f"🔍 Re-validate"):
                        revalidate_single_url(doc_id, cursor, conn)
                
                with col2:
                    if st.button(f"🗑️ Clear URL"):
                        clear_single_url(doc_id, cursor, conn)
                
                with col3:
                    new_url = st.text_input("Update URL:", key=f"url_{doc_id}")
                    if st.button("💾 Update URL") and new_url:
                        update_document_url(doc_id, new_url, cursor, conn)
        else:
            st.info("No URLs found in database")
            
    except Exception as e:
        st.error(f"Error displaying URL data: {e}")
    
    finally:
        cursor.close()
        conn.close()

def validate_all_urls_interface(cursor, conn):
    """Validate all URLs with progress tracking"""
    try:
        cursor.execute("""
            SELECT id, title, source 
            FROM documents 
            WHERE source IS NOT NULL AND source != '' AND source LIKE 'http%'
            ORDER BY id
        """)
        
        documents = cursor.fetchall()
        
        if not documents:
            st.info("No URLs found to validate")
            return
        
        st.info(f"Validating {len(documents)} URLs...")
        
        validator = URLValidator()
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        valid_count = 0
        invalid_count = 0
        
        for i, (doc_id, title, source_url) in enumerate(documents):
            status_text.text(f"Validating: {title[:40]}...")
            
            is_valid, status, redirect = validator.validate_url(source_url)
            
            if is_valid:
                valid_count += 1
            else:
                invalid_count += 1
            
            # Update database
            cursor.execute("""
                UPDATE documents 
                SET url_valid = %s, 
                    url_status = %s,
                    url_checked = CURRENT_TIMESTAMP
                WHERE id = %s
            """, (is_valid, status, doc_id))
            
            if redirect:
                cursor.execute("""
                    UPDATE documents 
                    SET source_redirect = %s
                    WHERE id = %s
                """, (redirect, doc_id))
            
            conn.commit()
            progress_bar.progress((i + 1) / len(documents))
        
        status_text.empty()
        progress_bar.empty()
        
        st.success(f"Validation complete: {valid_count} valid, {invalid_count} invalid URLs")
        st.rerun()
        
    except Exception as e:
        st.error(f"Validation error: {e}")

def revalidate_failed_urls(cursor, conn):
    """Re-validate only failed URLs"""
    try:
        cursor.execute("""
            SELECT id, title, source 
            FROM documents 
            WHERE url_valid = false
            ORDER BY id
        """)
        
        documents = cursor.fetchall()
        
        if not documents:
            st.info("No failed URLs to re-validate")
            return
        
        st.info(f"Re-validating {len(documents)} failed URLs...")
        
        validator = URLValidator()
        valid_count = 0
        
        for doc_id, title, source_url in documents:
            is_valid, status, redirect = validator.validate_url(source_url)
            
            if is_valid:
                valid_count += 1
                
                cursor.execute("""
                    UPDATE documents 
                    SET url_valid = %s, 
                        url_status = %s,
                        url_checked = CURRENT_TIMESTAMP
                    WHERE id = %s
                """, (is_valid, status, doc_id))
                
                if redirect:
                    cursor.execute("""
                        UPDATE documents 
                        SET source_redirect = %s
                        WHERE id = %s
                    """, (redirect, doc_id))
                
                conn.commit()
        
        if valid_count > 0:
            st.success(f"Re-validation complete: {valid_count} URLs now valid")
            st.rerun()
        else:
            st.warning("No previously failed URLs are now valid")
            
    except Exception as e:
        st.error(f"Re-validation error: {e}")

def clear_validation_data(cursor, conn):
    """Clear all validation data"""
    try:
        cursor.execute("""
            UPDATE documents 
            SET url_valid = NULL, 
                url_status = NULL, 
                url_checked = NULL,
                source_redirect = NULL
            WHERE source IS NOT NULL
        """)
        conn.commit()
        
        st.success("All validation data cleared")
        st.rerun()
        
    except Exception as e:
        st.error(f"Error clearing validation data: {e}")

def revalidate_single_url(doc_id, cursor, conn):
    """Re-validate a single URL"""
    try:
        cursor.execute("SELECT source FROM documents WHERE id = %s", (doc_id,))
        result = cursor.fetchone()
        
        if result:
            source_url = result[0]
            is_valid, status = validate_single_url(source_url)
            
            cursor.execute("""
                UPDATE documents 
                SET url_valid = %s, 
                    url_status = %s,
                    url_checked = CURRENT_TIMESTAMP
                WHERE id = %s
            """, (is_valid, status, doc_id))
            
            conn.commit()
            
            if is_valid:
                st.success(f"URL is now valid: {status}")
            else:
                st.error(f"URL is still invalid: {status}")
            
            st.rerun()
            
    except Exception as e:
        st.error(f"Error re-validating URL: {e}")

def clear_single_url(doc_id, cursor, conn):
    """Clear URL for a single document"""
    try:
        cursor.execute("""
            UPDATE documents 
            SET source = NULL,
                url_valid = NULL,
                url_status = NULL,
                url_checked = NULL,
                source_redirect = NULL
            WHERE id = %s
        """, (doc_id,))
        
        conn.commit()
        st.success("URL cleared for document")
        st.rerun()
        
    except Exception as e:
        st.error(f"Error clearing URL: {e}")

def update_document_url(doc_id, new_url, cursor, conn):
    """Update URL for a document"""
    try:
        # Validate new URL first
        is_valid, status = validate_single_url(new_url)
        
        cursor.execute("""
            UPDATE documents 
            SET source = %s,
                url_valid = %s,
                url_status = %s,
                url_checked = CURRENT_TIMESTAMP
            WHERE id = %s
        """, (new_url, is_valid, status, doc_id))
        
        conn.commit()
        
        if is_valid:
            st.success(f"URL updated and validated: {status}")
        else:
            st.warning(f"URL updated but validation failed: {status}")
        
        st.rerun()
        
    except Exception as e:
        st.error(f"Error updating URL: {e}")

if __name__ == "__main__":
    render()