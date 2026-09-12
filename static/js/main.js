// Global variables
let sessionId = document.querySelector('meta[name="session-id"]')?.content || '';
let currentContext = '';

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    // Get session ID from cookie or generate new one
    sessionId = getCookie('session_id') || generateSessionId();
    setCookie('session_id', sessionId, 7);
    
    // Event listeners
    document.getElementById('submitQuery').addEventListener('click', submitQuery);
    document.getElementById('queryInput').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') submitQuery();
    });
    
    document.getElementById('submitFollowup').addEventListener('click', submitFollowup);
    document.getElementById('followupInput').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') submitFollowup();
    });
    
    document.getElementById('uploadBtn').addEventListener('click', function() {
        new bootstrap.Modal(document.getElementById('uploadModal')).show();
    });
    
    document.getElementById('uploadSubmit').addEventListener('click', uploadFile);
    document.getElementById('resetBtn').addEventListener('click', resetSession);
    
    // Sample queries
    document.querySelectorAll('.sample-query').forEach(btn => {
        btn.addEventListener('click', function() {
            document.getElementById('queryInput').value = this.textContent;
            submitQuery();
        });
    });
});

// Submit main query
async function submitQuery() {
    const query = document.getElementById('queryInput').value.trim();
    if (!query) return;
    
    // Show loading
    document.getElementById('loadingProgress').style.display = 'block';
    document.getElementById('emptyState').style.display = 'none';
    document.getElementById('dashboardContent').style.display = 'none';
    
    try {
        const response = await fetch('/query', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                query: query,
                session_id: sessionId
            })
        });
        
        const data = await response.json();
        
        if (data.error) {
            alert('Error: ' + data.error);
            return;
        }
        
        // Update dashboard
        updateDashboard(data);
        currentContext = query;
        
        // Add to history
        addToHistory(query, data.dashboard_title);
        
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to generate dashboard');
    } finally {
        document.getElementById('loadingProgress').style.display = 'none';
    }
}

// Update dashboard with response data
function updateDashboard(data) {
    // Show dashboard
    document.getElementById('dashboardContent').style.display = 'block';
    
    // Update title
    document.getElementById('dashboardTitle').textContent = data.dashboard_title || 'Dashboard';
    document.getElementById('recordCount').textContent = `Showing ${data.total_records || 0} records`;
    
    // Update KPIs
    const kpiContainer = document.getElementById('kpiCards');
    kpiContainer.innerHTML = '';
    
    if (data.kpis && data.kpis.length > 0) {
        data.kpis.forEach(kpi => {
            kpiContainer.innerHTML += `
                <div class="col-md-3 mb-3">
                    <div class="card kpi-card">
                        <div class="card-body">
                            <h6 class="card-subtitle mb-2 text-muted">${kpi.icon} ${kpi.title}</h6>
                            <h3 class="card-title">${kpi.value}</h3>
                            <span class="badge bg-success">${kpi.change}</span>
                        </div>
                    </div>
                </div>
            `;
        });
    }
    
    // Update charts
    const chartsContainer = document.getElementById('chartsGrid');
    chartsContainer.innerHTML = '';
    
    if (data.charts && data.charts.length > 0) {
        data.charts.forEach((chart, index) => {
            chartsContainer.innerHTML += `
                <div class="col-md-6 mb-4">
                    <div class="card chart-card">
                        <div class="card-header">
                            <h6 class="mb-0">${chart.title}</h6>
                        </div>
                        <div class="card-body">
                            <div id="chart-${index}"></div>
                        </div>
                    </div>
                </div>
            `;
            
            // Render chart
            setTimeout(() => {
                const chartDiv = document.getElementById(`chart-${index}`);
                if (chartDiv) {
                    chartDiv.innerHTML = chart.html;
                }
            }, 100);
        });
    }
    
    // Update insights
    document.getElementById('insightsContent').innerHTML = 
        `<div class="insights-text">${data.insights.replace(/\n/g, '<br>')}</div>`;
    
    // Update SQL
    document.getElementById('sqlQuery').textContent = data.sql_query;
}

// Submit follow-up question
async function submitFollowup() {
    const followup = document.getElementById('followupInput').value.trim();
    if (!followup) return;
    
    document.getElementById('loadingProgress').style.display = 'block';
    
    try {
        const response = await fetch('/followup', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                followup: followup,
                context: currentContext,
                session_id: sessionId
            })
        });
        
        const data = await response.json();
        
        if (data.error) {
            alert('Error: ' + data.error);
            return;
        }
        
        // Update dashboard
        updateDashboard(data);
        currentContext = followup;
        
        // Clear input
        document.getElementById('followupInput').value = '';
        
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to process follow-up');
    } finally {
        document.getElementById('loadingProgress').style.display = 'none';
    }
}

// Upload CSV file
async function uploadFile() {
    const fileInput = document.getElementById('csvFile');
    const file = fileInput.files[0];
    
    if (!file) {
        alert('Please select a file');
        return;
    }
    
    const formData = new FormData();
    formData.append('file', file);
    
    // Show upload progress
    document.getElementById('uploadProgress').style.display = 'block';
    const progressBar = document.querySelector('#uploadProgress .progress-bar');
    
    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.error) {
            alert('Upload error: ' + data.error);
        } else {
            alert('File uploaded successfully!');
            
            // Update data source info
            if (data.table_info) {
                updateDataSourceInfo(data.table_info);
            }
            
            // Close modal
            bootstrap.Modal.getInstance(document.getElementById('uploadModal')).hide();
        }
        
    } catch (error) {
        console.error('Upload error:', error);
        alert('Failed to upload file');
    } finally {
        document.getElementById('uploadProgress').style.display = 'none';
        progressBar.style.width = '0%';
    }
}

// Reset session
async function resetSession() {
    try {
        const response = await fetch('/reset', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });
        
        const data = await response.json();
        
        if (data.success) {
            sessionId = data.session_id;
            setCookie('session_id', sessionId, 7);
            
            // Reset UI
            document.getElementById('dashboardContent').style.display = 'none';
            document.getElementById('emptyState').style.display = 'block';
            document.getElementById('queryInput').value = '';
            document.getElementById('historyList').innerHTML = '<p class="text-muted text-center">No queries yet</p>';
        }
        
    } catch (error) {
        console.error('Reset error:', error);
    }
}

// Add query to history
function addToHistory(query, title) {
    const historyList = document.getElementById('historyList');
    
    if (historyList.children.length === 1 && historyList.children[0].classList.contains('text-muted')) {
        historyList.innerHTML = '';
    }
    
    const historyItem = document.createElement('div');
    historyItem.className = 'history-item p-2 mb-2 bg-light rounded';
    historyItem.innerHTML = `
        <small class="text-primary">${title || 'Query'}</small>
        <p class="mb-0 small">${query.substring(0, 50)}${query.length > 50 ? '...' : ''}</p>
    `;
    
    historyList.insertBefore(historyItem, historyList.firstChild);
}

// Update data source info
function updateDataSourceInfo(tableInfo) {
    document.getElementById('tableName').textContent = tableInfo.table_name;
    
    const columnsList = document.getElementById('columnsList');
    columnsList.innerHTML = '';
    
    if (tableInfo.columns) {
        tableInfo.columns.forEach(col => {
            const li = document.createElement('li');
            li.textContent = `${col} (${tableInfo.dtypes[col]})`;
            columnsList.appendChild(li);
        });
    }
}

// Cookie helpers
function setCookie(name, value, days) {
    const expires = new Date();
    expires.setTime(expires.getTime() + days * 24 * 60 * 60 * 1000);
    document.cookie = `${name}=${value};expires=${expires.toUTCString()};path=/`;
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

function generateSessionId() {
    return 'session_' + Math.random().toString(36).substr(2, 9);
}