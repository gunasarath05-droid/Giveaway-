from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from .utils.scraper import scrape_instagram_comments
from .models import ScrapedPost, Comment

@api_view(['POST'])
def fetch_comments(request):
    url = request.data.get('url')
    print(f"📥 [API] Received request to fetch comments for: {url}")
    if not url:
        print("❌ [API] Missing URL in request data")
        return Response({"error": "URL is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    if "instagram.com" not in url:
        return Response({"error": "Invalid Instagram URL"}, status=status.HTTP_400_BAD_REQUEST)

    # Check for recent cached data (e.g., within 1 hour)
    cached_post = ScrapedPost.objects.filter(url=url).first()
    if cached_post and (timezone.now() - cached_post.updated_at < timedelta(hours=1)):
        comments_data = Comment.objects.filter(post=cached_post).order_by('-likes')[:10]
        if comments_data.exists():
            return Response([
                {"username": c.username, "comment": c.text, "likes": c.likes}
                for c in comments_data
            ])

    # If no cache or cache expired, run scraper
    try:
        scraped_data = scrape_instagram_comments(url)
        if not scraped_data:
            return Response({"error": "No comments found or unable to scrape."}, status=status.HTTP_404_NOT_FOUND)
        
        # Persist to MongoDB
        post, created = ScrapedPost.objects.update_or_create(
            url=url,
            defaults={'updated_at': timezone.now()}
        )
        
        # Clear existing comments for this post before refreshing
        Comment.objects.filter(post=post).delete()
        
        # Save new comments
        for item in scraped_data:
            Comment.objects.create(
                post=post,
                username=item['username'],
                text=item['comment'],
                likes=item['likes']
            )
            
        return Response(scraped_data)
        
    except Exception as e:
        print(f"❌ [API] Internal error: {str(e)}")
        # Fallback to cache if scraping fails
        if cached_post:
            print("🔄 [API] Falling back to cached comments...")
            comments_data = Comment.objects.filter(post=cached_post).order_by('-likes')[:10]
            if comments_data.exists():
                return Response([
                    {"username": c.username, "comment": c.text, "likes": c.likes}
                    for c in comments_data
                ])
        return Response({"error": f"Scraping failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
