import os
from supabase_client import supabase

class CompanyRepository:
    def search_companies(self, query):
        # Only return companies that have at least one testimonial
        testimonial_company_ids = supabase.table('testimonials').select('company_id').execute()
        company_ids = list(set([t['company_id'] for t in testimonial_company_ids.data])) if testimonial_company_ids.data else []
        
        # If no testimonials exist, show all companies as fallback
        if not company_ids:
            print("No testimonials found in database, showing all companies as fallback")
            if query.strip():
                response = supabase.table('companies').select('*').ilike('name', f'%{query}%').execute()
            else:
                response = supabase.table('companies').select('*').execute()
            return response.data if response.data else []
        
        if query.strip():
            # Search by company name
            response = supabase.table('companies').select('*').ilike('name', f'%{query}%').in_('id', company_ids).execute()
        else:
            # Return all companies with testimonials when no query
            response = supabase.table('companies').select('*').in_('id', company_ids).execute()
        
        return response.data if response.data else []
    def get_company(self, company_id):
        response = supabase.table('companies').select('*').eq('id', company_id).single().execute()
        return response.data if response.data else None
    def get_company_by_user_id(self, user_id):
        response = supabase.table('companies').select('*').eq('user_id', user_id).execute()
        companies = response.data if response.data else []
        if len(companies) >= 1:
            return companies[0]
        else:
            return None 