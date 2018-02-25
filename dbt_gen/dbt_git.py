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

    def create_new_branch(self,branch):
        self.logger.debug("Creating new branch for table {}".format(branch))
        try:
            self.dgit.git.checkout('HEAD', b= self._prefix_branch(branch))
        except:
            self.logger.error('Failed to checkout new branch {} : {} '.format(self._prefix_branch(branch), sys.exc_info()))
            return False
        self.logger.debug('Created branch ' + self._prefix_branch(branch))
        return True

    def commit(self, branch):
        self.logger.debug("Committing file updates for {}".format(branch))
        try:
            self.dgit.git.add('--all')
            self.dgit.git.commit('-m','dbt_gen models and test generated for {}'.format(branch))
        except:
            self.logger.error('Failed to commit branch {} : {} '.format(self._prefix_branch(branch), sys.exc_info()))
            return False
        self.logger.debug('Committed branch '+ self._prefix_branch(branch))
        return True

    def push_to_origin(self, branch):
        self.logger.debug("Pushing to origin: {}".format(branch))
        try:
            self.dgit.git.push('origin',self._prefix_branch(branch))
        except:
            self.logger.error('Failed to push to origin {} : {} '.format(self._prefix_branch(branch), sys.exc_info()[0]))
            return False
        self.logger.debug('Pushed branch '+ self._prefix_branch(branch))
        return True

    def _prefix_branch(self,branch):
        return str('dbt_gen-template-for-' + branch)
