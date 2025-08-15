from ..repositories.company_repository import CompanyRepository

class CompanyService:
    def __init__(self):
        self.company_repository = CompanyRepository()

    def search_companies(self, query):
        return self.company_repository.search_companies(query)
    def get_company(self, company_id):
        return self.company_repository.get_company(company_id)
    def get_company_by_user_id(self, user_id):
        return self.company_repository.get_company_by_user_id(user_id) 