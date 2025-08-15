#!/usr/bin/env python3
"""
GitHub Review Scraper
Collects repository feedback including stars, issues, discussions, and PR comments.
"""

import requests
import json
import argparse
from datetime import datetime
import time
from typing import List, Dict, Optional
import logging
from dataclasses import dataclass

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class GitHubReview:
    """Data class to represent a GitHub feedback item"""
    title: str
    body: str
    author: str
    date: str
    type: str  # 'issue', 'discussion', 'pr_comment'
    url: str
    state: Optional[str] = None
    labels: List[str] = None
    reactions: Dict[str, int] = None
    rating: Optional[float] = None

class GitHubScraper:
    """Scraper for GitHub repository feedback"""
    
    def __init__(self, token: Optional[str] = None):
        """Initialize with optional GitHub token"""
        self.base_url = "https://api.github.com"
        self.session = requests.Session()
        if token:
            self.session.headers["Authorization"] = f"token {token}"
        self.session.headers["Accept"] = "application/vnd.github.v3+json"
        self.session.headers["User-Agent"] = "GitHubReviewScraper/1.0"
    
    def get_repo_info(self, owner: str, repo: str) -> Dict:
        """Get basic repository information"""
        url = f"{self.base_url}/repos/{owner}/{repo}"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()
    
    def get_issues(self, owner: str, repo: str, start_date: str, end_date: str) -> List[GitHubReview]:
        """Get repository issues within date range"""
        reviews = []
        page = 1
        
        while True:
            url = f"{self.base_url}/repos/{owner}/{repo}/issues"
            params = {
                "state": "all",
                "sort": "created",
                "direction": "desc",
                "per_page": 100,
                "page": page
            }
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            issues = response.json()
            
            if not issues:
                break
                
            for issue in issues:
                created_at = issue["created_at"][:10]  # YYYY-MM-DD
                if created_at < start_date:
                    return reviews
                if created_at <= end_date:
                    # Calculate rating based on reactions
                    reactions = issue.get("reactions", {})
                    total_reactions = sum(reactions.values())
                    positive = reactions.get("+1", 0) + reactions.get("heart", 0) + reactions.get("hooray", 0)
                    rating = (positive / total_reactions * 5) if total_reactions > 0 else None
                    
                    review = GitHubReview(
                        title=issue["title"],
                        body=issue["body"] or "",
                        author=issue["user"]["login"],
                        date=created_at,
                        type="issue",
                        url=issue["html_url"],
                        state=issue["state"],
                        labels=[label["name"] for label in issue["labels"]],
                        reactions=reactions,
                        rating=rating
                    )
                    reviews.append(review)
            
            page += 1
            time.sleep(1)  # Rate limiting
        
        return reviews
    
    def get_discussions(self, owner: str, repo: str, start_date: str, end_date: str) -> List[GitHubReview]:
        """Get repository discussions within date range"""
        reviews = []
        
        # Note: Discussions API requires GraphQL
        # For simplicity, we'll skip this for now
        # TODO: Implement GraphQL query for discussions
        
        return reviews
    
    def get_pr_comments(self, owner: str, repo: str, start_date: str, end_date: str) -> List[GitHubReview]:
        """Get pull request comments within date range"""
        reviews = []
        page = 1
        
        while True:
            url = f"{self.base_url}/repos/{owner}/{repo}/pulls/comments"
            params = {
                "sort": "created",
                "direction": "desc",
                "per_page": 100,
                "page": page
            }
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            comments = response.json()
            
            if not comments:
                break
                
            for comment in comments:
                created_at = comment["created_at"][:10]  # YYYY-MM-DD
                if created_at < start_date:
                    return reviews
                if created_at <= end_date:
                    review = GitHubReview(
                        title=f"PR Comment on {comment['pull_request_url'].split('/')[-1]}",
                        body=comment["body"],
                        author=comment["user"]["login"],
                        date=created_at,
                        type="pr_comment",
                        url=comment["html_url"],
                        reactions=comment.get("reactions", {}),
                    )
                    reviews.append(review)
            
            page += 1
            time.sleep(1)  # Rate limiting
        
        return reviews

def main():
    parser = argparse.ArgumentParser(description="Scrape GitHub repository feedback")
    parser.add_argument("--repo", required=True, help="Repository in format owner/repo")
    parser.add_argument("--start-date", required=True, help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end-date", required=True, help="End date (YYYY-MM-DD)")
    parser.add_argument("--token", help="GitHub API token")
    parser.add_argument("--output", default="github_reviews.json", help="Output JSON file")
    
    args = parser.parse_args()
    
    try:
        owner, repo = args.repo.split("/")
    except ValueError:
        logger.error("Invalid repository format. Use owner/repo")
        return
    
    scraper = GitHubScraper(args.token)
    
    try:
        # Get repo info first
        repo_info = scraper.get_repo_info(owner, repo)
        logger.info(f"Repository: {repo_info['full_name']}")
        logger.info(f"Stars: {repo_info['stargazers_count']}")
        logger.info(f"Description: {repo_info['description']}")
        
        # Get all types of feedback
        all_reviews = []
        
        # Get issues
        logger.info("Fetching issues...")
        issues = scraper.get_issues(owner, repo, args.start_date, args.end_date)
        all_reviews.extend(issues)
        logger.info(f"Found {len(issues)} issues")
        
        # Get PR comments
        logger.info("Fetching PR comments...")
        comments = scraper.get_pr_comments(owner, repo, args.start_date, args.end_date)
        all_reviews.extend(comments)
        logger.info(f"Found {len(comments)} PR comments")
        
        # Save results
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump([review.__dict__ for review in all_reviews], f, indent=2)
        
        logger.info(f"Saved {len(all_reviews)} reviews to {args.output}")
        
        # Print sample
        if all_reviews:
            print("\nSample review:")
            sample = all_reviews[0]
            print(f"Title: {sample.title}")
            print(f"Type: {sample.type}")
            print(f"Author: {sample.author}")
            print(f"Date: {sample.date}")
            if sample.rating:
                print(f"Rating: {sample.rating}")
            print(f"URL: {sample.url}")
    
    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {e}")
    except Exception as e:
        logger.error(f"Error: {e}")

if __name__ == "__main__":
    main()
