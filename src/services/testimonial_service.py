from ..repositories.testimonial_repository import TestimonialRepository

class TestimonialService:
    def __init__(self):
        self.testimonial_repository = TestimonialRepository()

    def get_testimonials_for_company(self, company_id):
        return self.testimonial_repository.get_testimonials_for_company(company_id)
    
    def get_all_testimonials_for_company(self, company_id):
        return self.testimonial_repository.get_all_testimonials_for_company(company_id)
    
    def get_testimonials_by_user(self, user_id):
        return self.testimonial_repository.get_testimonials_by_user(user_id)
    
    def add_testimonial(self, company_id, user_id, user_name, text):
        return self.testimonial_repository.add_testimonial(company_id, user_id, user_name, text)
    
    def add_testimonial_with_company(self, company_name, user_id, user_name, content, rating):
        """Add testimonial with company name - creates company if doesn't exist"""
        return self.testimonial_repository.add_testimonial_with_company(company_name, user_id, user_name, content, rating)
    
    def approve_testimonial(self, testimonial_id):
        return self.testimonial_repository.approve_testimonial(testimonial_id)
    
    def reject_testimonial(self, testimonial_id):
        return self.testimonial_repository.reject_testimonial(testimonial_id)
    
    def get_testimonial_stats_for_company(self, company_id):
        return self.testimonial_repository.get_testimonial_stats_for_company(company_id)
    
    def get_testimonial_stats_for_user(self, user_id):
        return self.testimonial_repository.get_testimonial_stats_for_user(user_id)
    
    def like_testimonial(self, testimonial_id):
        return self.testimonial_repository.like_testimonial(testimonial_id)
    
    def add_comment(self, testimonial_id, user_id, user_name, text):
        return self.testimonial_repository.add_comment(testimonial_id, user_id, user_name, text)
    
    def get_comments_for_testimonial(self, testimonial_id):
        return self.testimonial_repository.get_comments_for_testimonial(testimonial_id)
    
    def add_comment_to_testimonial(self, testimonial_id, user_id, user_name, text):
        return self.testimonial_repository.add_comment_to_testimonial(testimonial_id, user_id, user_name, text) 