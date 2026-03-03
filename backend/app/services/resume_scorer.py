import re

def score_resume(resume_info, job_description):
    """
    Calculate resume-job matching score
    """
    # Extract keywords from job description
    job_keywords = extract_keywords(job_description)
    
    # Extract keywords from resume
    resume_keywords = extract_resume_keywords(resume_info)
    
    # Calculate skill match score
    skill_match_score = calculate_skill_match(job_keywords, resume_keywords)
    
    # Calculate experience match score
    experience_match_score = calculate_experience_match(resume_info, job_description)
    
    # Calculate education match score
    education_match_score = calculate_education_match(resume_info, job_description)
    
    # Calculate final score (weighted average)
    final_score = (skill_match_score * 0.5) + (experience_match_score * 0.3) + (education_match_score * 0.2)
    
    return {
        'overall_score': round(final_score, 2),
        'skill_match': round(skill_match_score, 2),
        'experience_match': round(experience_match_score, 2),
        'education_match': round(education_match_score, 2),
        'matched_keywords': find_matched_keywords(job_keywords, resume_keywords)
    }

def extract_keywords(text):
    """
    Extract keywords from text
    """
    # Convert to lowercase and split into words
    text = text.lower()
    
    # Remove punctuation
    text = re.sub(r'[\W_]+', ' ', text)
    
    # Split into words
    words = text.split()
    
    # Remove common stop words
    stop_words = {'the', 'and', 'of', 'in', 'to', 'for', 'with', 'on', 'at', 'by', 'from', 'as', 'is', 'are', 'was', 'were', 'be', 'been', 'being'}
    keywords = [word for word in words if word not in stop_words and len(word) > 2]
    
    # Return unique keywords
    return list(set(keywords))

def extract_resume_keywords(resume_info):
    """
    Extract keywords from resume information
    """
    all_text = ''
    
    # Combine all resume information into a single text
    if resume_info.get('basic_info'):
        all_text += ' '.join(resume_info['basic_info'].values()) + ' '
    
    if resume_info.get('job_info'):
        all_text += ' '.join(resume_info['job_info'].values()) + ' '
    
    if resume_info.get('background_info'):
        all_text += ' '.join(resume_info['background_info'].values()) + ' '
    
    # Extract keywords
    return extract_keywords(all_text)

def calculate_skill_match(job_keywords, resume_keywords):
    """
    Calculate skill match score
    """
    if not job_keywords:
        return 1.0
    
    # Count matched keywords
    matched = 0
    for keyword in job_keywords:
        if keyword in resume_keywords:
            matched += 1
    
    # Calculate match percentage
    return matched / len(job_keywords)

def calculate_experience_match(resume_info, job_description):
    """
    Calculate experience match score
    """
    # Extract work experience from resume
    work_experience = resume_info.get('background_info', {}).get('work_experience', '')
    
    # Look for experience-related keywords in job description
    experience_keywords = ['experience', 'years', '年', '经验', 'work', 'employment']
    job_lower = job_description.lower()
    
    # Check if job description mentions experience requirements
    has_experience_req = any(keyword in job_lower for keyword in experience_keywords)
    
    if not has_experience_req:
        return 1.0
    
    # Check if resume has work experience
    if work_experience:
        return 0.8
    else:
        return 0.3

def calculate_education_match(resume_info, job_description):
    """
    Calculate education match score
    """
    # Extract education from resume
    education = resume_info.get('background_info', {}).get('education', '')
    
    # Look for education-related keywords in job description
    education_keywords = ['education', 'degree', '学历', '本科', '硕士', '博士', 'bachelor', 'master', 'phd']
    job_lower = job_description.lower()
    
    # Check if job description mentions education requirements
    has_education_req = any(keyword in job_lower for keyword in education_keywords)
    
    if not has_education_req:
        return 1.0
    
    # Check if resume has education information
    if education:
        return 0.8
    else:
        return 0.3

def find_matched_keywords(job_keywords, resume_keywords):
    """
    Find matched keywords between job description and resume
    """
    return [keyword for keyword in job_keywords if keyword in resume_keywords]
