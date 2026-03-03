import re

def extract_info(text):
    """
    Extract key information from resume text
    """
    info = {
        'basic_info': {
            'name': extract_name(text),
            'phone': extract_phone(text),
            'email': extract_email(text),
            'address': extract_address(text)
        },
        'job_info': {
            'intention': extract_intention(text),
            'salary': extract_salary(text)
        },
        'background_info': {
            'work_experience': extract_work_experience(text),
            'education': extract_education(text),
            'projects': extract_projects(text)
        }
    }
    return info

def extract_name(text):
    """
    Extract name from resume text
    """
    # Simple pattern for Chinese names (2-4 characters)
    chinese_name_pattern = r'[\u4e00-\u9fa5]{2,4}'
    # Simple pattern for English names (first and last name)
    english_name_pattern = r'[A-Z][a-z]+\s+[A-Z][a-z]+'
    
    # Try to find Chinese name first
    chinese_match = re.search(chinese_name_pattern, text)
    if chinese_match:
        return chinese_match.group()
    
    # Try to find English name
    english_match = re.search(english_name_pattern, text)
    if english_match:
        return english_match.group()
    
    return ""

def extract_phone(text):
    """
    Extract phone number from resume text
    """
    phone_pattern = r'1[3-9]\d{9}'
    match = re.search(phone_pattern, text)
    if match:
        return match.group()
    return ""

def extract_email(text):
    """
    Extract email address from resume text
    """
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    match = re.search(email_pattern, text)
    if match:
        return match.group()
    return ""

def extract_address(text):
    """
    Extract address from resume text
    """
    # Simple pattern for Chinese addresses
    address_pattern = r'[\u4e00-\u9fa5]{2,}(省|市|区|县|镇|街道|路|号)[^\n]+'
    match = re.search(address_pattern, text)
    if match:
        return match.group()
    return ""

def extract_intention(text):
    """
    Extract job intention from resume text
    """
    # Look for sections related to job intention
    intention_keywords = ['求职意向', '应聘职位', '意向岗位', 'position', 'intention']
    lines = text.split('\n')
    
    for i, line in enumerate(lines):
        line_lower = line.lower()
        for keyword in intention_keywords:
            if keyword.lower() in line_lower:
                # Return the next line as intention
                if i + 1 < len(lines):
                    return lines[i + 1]
                return line
    
    return ""

def extract_salary(text):
    """
    Extract expected salary from resume text
    """
    # Pattern for salary information
    salary_pattern = r'期望薪资[:：]?\s*([^\n]+)|\$?\d+(,\d{3})*\s*[-–]\s*\$?\d+(,\d{3})*|\d+\s*K\s*[-–]\s*\d+\s*K'
    match = re.search(salary_pattern, text, re.IGNORECASE)
    if match:
        return match.group()
    return ""

def extract_work_experience(text):
    """
    Extract work experience from resume text
    """
    # Look for sections related to work experience
    experience_keywords = ['工作经验', '实习经历', 'employment', 'work experience', 'internship']
    lines = text.split('\n')
    experience_lines = []
    
    in_experience_section = False
    for line in lines:
        line_lower = line.lower()
        
        # Check if we're entering an experience section
        if any(keyword in line_lower for keyword in experience_keywords):
            in_experience_section = True
            continue
        
        # Check if we're exiting the experience section (when encountering other sections)
        if in_experience_section and any(section in line_lower for section in ['教育背景', 'education', '项目经历', 'projects', '技能', 'skills']):
            break
        
        if in_experience_section and line.strip():
            experience_lines.append(line)
    
    return '\n'.join(experience_lines)

def extract_education(text):
    """
    Extract education background from resume text
    """
    # Look for sections related to education
    education_keywords = ['教育背景', '学历', 'education', 'academic background']
    lines = text.split('\n')
    education_lines = []
    
    in_education_section = False
    for line in lines:
        line_lower = line.lower()
        
        # Check if we're entering an education section
        if any(keyword in line_lower for keyword in education_keywords):
            in_education_section = True
            continue
        
        # Check if we're exiting the education section
        if in_education_section and any(section in line_lower for section in ['工作经验', 'employment', '项目经历', 'projects', '技能', 'skills']):
            break
        
        if in_education_section and line.strip():
            education_lines.append(line)
    
    return '\n'.join(education_lines)

def extract_projects(text):
    """
    Extract project experience from resume text
    """
    # Look for sections related to projects
    project_keywords = ['项目经历', '项目经验', 'projects', 'project experience']
    lines = text.split('\n')
    project_lines = []
    
    in_project_section = False
    for line in lines:
        line_lower = line.lower()
        
        # Check if we're entering a project section
        if any(keyword in line_lower for keyword in project_keywords):
            in_project_section = True
            continue
        
        # Check if we're exiting the project section
        if in_project_section and any(section in line_lower for section in ['工作经验', 'employment', '教育背景', 'education', '技能', 'skills']):
            break
        
        if in_project_section and line.strip():
            project_lines.append(line)
    
    return '\n'.join(project_lines)
