// 全局变量，存储解析后的简历信息
let resumeInfo = null;

// 页面加载完成后绑定事件
document.addEventListener('DOMContentLoaded', function() {
    // 绑定上传表单提交事件
    document.getElementById('upload-form').addEventListener('submit', function(e) {
        e.preventDefault();
        uploadResume();
    });
    
    // 绑定匹配表单提交事件
    document.getElementById('match-form').addEventListener('submit', function(e) {
        e.preventDefault();
        calculateMatch();
    });
});

// 上传简历并解析
function uploadResume() {
    const fileInput = document.getElementById('resume-file');
    const file = fileInput.files[0];
    
    if (!file) {
        alert('请选择PDF文件');
        return;
    }
    
    const formData = new FormData();
    formData.append('file', file);
    
    // 显示加载状态
    const parseResult = document.getElementById('parse-result');
    parseResult.innerHTML = '<p>正在解析简历，请稍候...</p>';
    document.getElementById('result-section').style.display = 'block';
    
    // 发送请求到后端
    fetch('http://localhost:5000/api/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            parseResult.innerHTML = `<p style="color: red;">错误: ${data.error}</p>`;
        } else {
            // 存储简历信息
            resumeInfo = data.info;
            
            // 显示解析结果
            displayParseResult(data);
            
            // 显示岗位匹配区域
            document.getElementById('match-section').style.display = 'block';
        }
    })
    .catch(error => {
        parseResult.innerHTML = `<p style="color: red;">上传失败: ${error.message}</p>`;
    });
}

// 显示解析结果
function displayParseResult(data) {
    const parseResult = document.getElementById('parse-result');
    const info = data.info;
    
    let html = `
        <div class="info-block">
            <h3>基本信息</h3>
            <div class="info-item"><strong>姓名:</strong> ${info.basic_info.name || '未找到'}</div>
            <div class="info-item"><strong>电话:</strong> ${info.basic_info.phone || '未找到'}</div>
            <div class="info-item"><strong>邮箱:</strong> ${info.basic_info.email || '未找到'}</div>
            <div class="info-item"><strong>地址:</strong> ${info.basic_info.address || '未找到'}</div>
        </div>
        
        <div class="info-block">
            <h3>求职信息</h3>
            <div class="info-item"><strong>求职意向:</strong> ${info.job_info.intention || '未找到'}</div>
            <div class="info-item"><strong>期望薪资:</strong> ${info.job_info.salary || '未找到'}</div>
        </div>
        
        <div class="info-block">
            <h3>背景信息</h3>
            <div class="info-item"><strong>工作经验:</strong> ${info.background_info.work_experience ? '有' : '未找到'}</div>
            <div class="info-item"><strong>教育背景:</strong> ${info.background_info.education ? '有' : '未找到'}</div>
            <div class="info-item"><strong>项目经历:</strong> ${info.background_info.projects ? '有' : '未找到'}</div>
        </div>
    `;
    
    parseResult.innerHTML = html;
}

// 计算岗位匹配度
function calculateMatch() {
    if (!resumeInfo) {
        alert('请先上传并解析简历');
        return;
    }
    
    const jobDescription = document.getElementById('job-description').value;
    if (!jobDescription) {
        alert('请输入岗位需求描述');
        return;
    }
    
    // 显示加载状态
    const matchResult = document.getElementById('match-result');
    matchResult.innerHTML = '<p>正在计算匹配度，请稍候...</p>';
    
    // 发送请求到后端
    fetch('http://localhost:5000/api/score', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            resume_info: resumeInfo,
            job_description: jobDescription
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            matchResult.innerHTML = `<p style="color: red;">错误: ${data.error}</p>`;
        } else {
            // 显示匹配结果
            displayMatchResult(data.score);
        }
    })
    .catch(error => {
        matchResult.innerHTML = `<p style="color: red;">计算失败: ${error.message}</p>`;
    });
}

// 显示匹配结果
function displayMatchResult(score) {
    const matchResult = document.getElementById('match-result');
    
    let html = `
        <div class="score-card">
            <div class="overall-score">总体匹配度: ${score.overall_score * 100}%</div>
            <div class="score-item"><span>技能匹配:</span> <span>${score.skill_match * 100}%</span></div>
            <div class="score-item"><span>经验匹配:</span> <span>${score.experience_match * 100}%</span></div>
            <div class="score-item"><span>教育匹配:</span> <span>${score.education_match * 100}%</span></div>
            
            <div class="matched-keywords">
                <strong>匹配的关键词:</strong>
                <ul>
                    ${score.matched_keywords.map(keyword => `<li>${keyword}</li>`).join('')}
                </ul>
            </div>
        </div>
    `;
    
    matchResult.innerHTML = html;
}
