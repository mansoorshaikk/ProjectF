import os
from supabase_client import supabase

class TestimonialRepository:
    def get_testimonials_for_company(self, company_id):
        # Only show approved testimonials publicly
        response = supabase.table('testimonials').select('*').eq('company_id', company_id).eq('status', 'approved').order('created_at', desc=True).execute()
        return response.data if response.data else []
    
    def get_all_testimonials_for_company(self, company_id):
        # Get all testimonials (including pending) for company dashboard
        response = supabase.table('testimonials').select('*').eq('company_id', company_id).order('created_at', desc=True).execute()
        return response.data if response.data else []
    
    def get_testimonials_by_user(self, user_id):
        response = supabase.table('testimonials').select('*').eq('user_id', user_id).order('created_at', desc=True).execute()
        return response.data if response.data else []
    
    def add_testimonial(self, company_id, user_id, user_name, text):
        # Check if company exists before inserting
        company_response = supabase.table('companies').select('id').eq('id', company_id).execute()
        if not company_response.data or len(company_response.data) == 0:
            print(f"[Warning] Tried to add testimonial for non-existent company_id: {company_id}")
            return None
        response = supabase.table('testimonials').insert({
            'company_id': company_id,
            'user_id': user_id,
            'user_name': user_name,
            'text': text,
            'likes': 0,
            'status': 'pending'  # Default status is pending
        }).execute()
        if not response.data:
            print(f"[Error] Failed to insert testimonial for company_id: {company_id}, user_id: {user_id}, response: {response}")
            if hasattr(response, 'error'):
                print(f"[Error details]: {response.error}")
            return None
        return response.data[0]
    
    def add_testimonial_with_company(self, company_name, user_id, user_name, content, rating):
        """Add testimonial with company name - creates company if doesn't exist"""
        # First, try to find existing company
        company_response = supabase.table('companies').select('id').eq('name', company_name).execute()
        
        if company_response.data and len(company_response.data) > 0:
            company_id = company_response.data[0]['id']
        else:
            # Create new company
            company_response = supabase.table('companies').insert({
                'name': company_name,
                'user_id': user_id  # Link to the user creating the testimonial
            }).execute()
            if not company_response.data:
                print(f"[Error] Failed to create company: {company_name}")
                return None
            company_id = company_response.data[0]['id']
        
        # Add testimonial with existing schema
        testimonial_data = {
            'company_id': company_id,
            'user_id': user_id,
            'user_name': user_name,
            'text': content,
            'likes': 0,
            'status': 'pending'  # Default status is pending
        }
        
        # Only add rating if it's a valid number and greater than 0
        if rating and isinstance(rating, (int, float)) and rating > 0:
            try:
                testimonial_data['rating'] = int(rating)
            except (ValueError, TypeError):
                # If rating can't be converted to int, skip it
                pass
        
        response = supabase.table('testimonials').insert(testimonial_data).execute()
        
        if not response.data:
            print(f"[Error] Failed to insert testimonial for company: {company_name}")
            return None
        return response.data[0]
    
    def approve_testimonial(self, testimonial_id):
        """Approve a testimonial"""
        response = supabase.table('testimonials').update({'status': 'approved'}).eq('id', testimonial_id).execute()
        return response.data[0] if response.data else None
    
    def reject_testimonial(self, testimonial_id):
        """Reject a testimonial"""
        response = supabase.table('testimonials').update({'status': 'rejected'}).eq('id', testimonial_id).execute()
        return response.data[0] if response.data else None
    
    def get_testimonial_stats_for_company(self, company_id):
        """Get testimonial statistics for a company"""
        # Get all testimonials for the company
        response = supabase.table('testimonials').select('*').eq('company_id', company_id).execute()
        testimonials = response.data if response.data else []
        
        stats = {
            'total': len(testimonials),
            'pending': len([t for t in testimonials if t.get('status') == 'pending']),
            'approved': len([t for t in testimonials if t.get('status') == 'approved']),
            'rejected': len([t for t in testimonials if t.get('status') == 'rejected']),
            'average_rating': 0
        }
        
        # Calculate average rating from approved testimonials
        approved_with_ratings = [t for t in testimonials if t.get('status') == 'approved' and t.get('rating')]
        if approved_with_ratings:
            total_rating = sum(t.get('rating', 0) for t in approved_with_ratings)
            stats['average_rating'] = round(total_rating / len(approved_with_ratings), 1)
        
        return stats
    
    def get_testimonial_stats_for_user(self, user_id):
        """Get testimonial statistics for a user"""
        response = supabase.table('testimonials').select('*').eq('user_id', user_id).execute()
        testimonials = response.data if response.data else []
        
        stats = {
            'total': len(testimonials),
            'pending': len([t for t in testimonials if t.get('status') == 'pending']),
            'approved': len([t for t in testimonials if t.get('status') == 'approved']),
            'rejected': len([t for t in testimonials if t.get('status') == 'rejected'])
        }
        
        return stats
    
    def like_testimonial(self, testimonial_id):
        testimonial = supabase.table('testimonials').select('likes').eq('id', testimonial_id).single().execute().data
        new_likes = (testimonial['likes'] if testimonial else 0) + 1
        response = supabase.table('testimonials').update({'likes': new_likes}).eq('id', testimonial_id).execute()
        return new_likes
    
    def add_comment(self, testimonial_id, user_id, user_name, text):
        # Comments are stored as a JSONB array in the testimonial row
        testimonial = supabase.table('testimonials').select('comments').eq('id', testimonial_id).single().execute().data
        comments = testimonial['comments'] if testimonial and testimonial.get('comments') else []
        comment = {'user_id': user_id, 'user_name': user_name, 'text': text}
        comments.append(comment)
        supabase.table('testimonials').update({'comments': comments}).eq('id', testimonial_id).execute()
        return comment
    
    def get_comments_for_testimonial(self, testimonial_id):
        """Get comments for a testimonial from the comments table"""
        try:
            response = supabase.table('comments').select('*').eq('testimonial_id', testimonial_id).order('created_at', desc=False).execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"[Error] Failed to get comments for testimonial {testimonial_id}: {e}")
            return []
    
    def add_comment_to_testimonial(self, testimonial_id, user_id, user_name, text):
        """Add a comment to a testimonial using the comments table"""
        try:
            comment_data = {
                'testimonial_id': testimonial_id,
                'user_id': user_id,
                'user_name': user_name,
                'text': text
            }
            
            response = supabase.table('comments').insert(comment_data).execute()
            
            if response.data:
                return response.data[0]
            else:
                print(f"[Error] Failed to insert comment for testimonial: {testimonial_id}")
                return None
        except Exception as e:
            print(f"[Error] Failed to add comment to testimonial {testimonial_id}: {e}")
            return None 