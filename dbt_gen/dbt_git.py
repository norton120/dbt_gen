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
        self.logger.debug('Repo on master')
        return True

    def create_new_branch(self,table):
        self.logger.debug("Creating new branch for table {}".format(table))
        try:
            self.dgit.git.checkout('HEAD', b='dbt_gen-template-for-'+table)
        except:
            self.logger.error('Failed to checkout new branch dbt_gen-template-for-{} : {} '.format(table, sys.exc_info()[0]))
            return False
        self.logger.debug('Created branch dbt_gen-template-for-'+table)
        return True
