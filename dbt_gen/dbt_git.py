import git
import sys
from global_logger import GLOBAL_LOGGER

class dbt_git():

    logger = GLOBAL_LOGGER
                           

    def __init__(self,repo):
        self.dgit= git.Repo(repo)
        
    def prep_repo(self):
        self.logger.debug("Preparing repo")
        try:
            self.dgit.git.checkout('master')
            self.dgit.git.pull()
        except:
            self.logger.error('Failed to prepare repo for new branch.')
            return False
        self.logger.debug('Repo prepared for new branch')
        return True

#        return self.checkout('HEAD', b=branch_name)

