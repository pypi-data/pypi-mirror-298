import filecmp
import os
import shutil

from ..cfg import Cfg
from ..utils_logger import UtilsLogger as log


# --------------------
## for Dev purposes to help update repos to common states
class App:
    # --------------------
    ## constructor
    def __init__(self):
        ## the tech: python, cpp, arduino
        self._repo_tech = 'unset'
        ## repo type: app, module, both
        self._repo_type = 'unset'
        ## repo name
        self._repo_name = 'unset'
        ## repo name
        self._repo_dir = 'unset'
        ## template file rootdir
        self._template_rootdir = os.path.join('tools', 'xplat_utils', 'templates')

        ## number of meld instances popped up
        self._meld_count = 0
        ## show meld for any non-matching files
        self._show_meld = True

    # --------------------
    ## initialize
    #
    # @return None
    def init(self):
        log.highlight('Info')
        self._repo_name = os.popen('git rev-parse --show-toplevel').read()
        self._repo_name = os.path.basename(self._repo_name).strip()
        log.line(f'   {"repo": <10}: {self._repo_name}')

        cfg = Cfg()
        cfg.load('.')

        self._repo_dir = cfg.mod_dir_name

        self._repo_tech = cfg.mod_tech
        log.line(f'   {"tech": <10}: {self._repo_tech}')

        if cfg.is_module:
            self._repo_type = 'module'
        else:
            self._repo_type = 'app'
        log.line(f'   {"type": <10}: {self._repo_type}')

        log.line('-------')

        if self._repo_tech == 'arduino' and self._repo_type == 'module':
            self._abort('arduino modules are invalid')

    # --------------------
    ## terminate
    #
    # @return None
    def term(self):
        pass

    # --------------------
    ## check all files and update as necessary
    #
    # @return None
    def run(self):
        self._meld_count = 0
        for curr_file, info_list in sorted(self.files_to_check.items()):
            found = False
            for info in info_list:
                template_file = info['template']
                doit, _ = self._get_doit(curr_file, template_file, info)
                if not doit:
                    continue

                # handle it on the first match
                found = True
                self._handle_check_template(curr_file, template_file)
                break

            if not found:
                if not os.path.isfile(curr_file):
                    self._log_file(curr_file, 'OK', 'file not found, skipping')
                else:
                    self._log_file(curr_file, 'CHK', 'not applicable, skipping')

        self._handle_common_files()
        self._handle_medver_files()
        log.line(f'opened {self._meld_count} meld instances')

        log.start('double-check all files are handled')
        self._dev_double_check()

    # --------------------
    ## check if whether the file can be skipped or not
    #
    # @param curr_file      path to current file
    # @param template_file  the template file name
    # @param info           the info from the check_info below
    # @return True if the file should be compared, otherwise false
    def _get_doit(self, curr_file, template_file, info):
        # for dbg
        reasons = f'{template_file}: skipped reasons: '

        # check against tech
        if isinstance(info['tech'], str) and info['tech'] == 'all':
            tech_ok = True
        elif self._repo_tech in info['tech']:
            tech_ok = True
        else:
            tech_ok = False
            reasons += 'tech '

        # check against type
        if isinstance(info['type'], str) and info['type'] == 'all':
            type_ok = True
        elif self._repo_type in info['type']:
            type_ok = True
        else:
            type_ok = False
            reasons += 'type '

        # check if this repo is specifically included/excluded
        repo_ok = True
        if self._repo_name in info['repos']:
            action = info['repos'][self._repo_name]
            if action not in ['skip', 'include']:
                self._abort(f'{curr_file: <20}: unknown action:{action} for repo:{self._repo_name}')
            elif action == 'skip':
                repo_ok = False
                reasons += 'repo '
            elif action == 'include':
                repo_ok = True
                tech_ok = True  # override if false
                type_ok = True  # override if false

        doit = tech_ok and type_ok and repo_ok
        # log.dbg(f'curr_file: {curr_file} tech_ok: {tech_ok} type: {type_ok} repo_ok: {repo_ok} doit: {doit}')

        return doit, reasons

    # --------------------
    ## check file if it exists and if it is differeant than the template
    #
    # @param curr_file  path to current file
    # @param tmp_file   template file name
    # @return None
    def _handle_check_template(self, curr_file, tmp_file):
        template = os.path.join(self._template_rootdir, tmp_file)

        if not os.path.isfile(curr_file):
            self._handle_missing_file(curr_file, template)
            self._log_file(curr_file, 'OK', f'missing, copied from {tmp_file}')
        else:
            matches = filecmp.cmp(curr_file, template, shallow=False)
            if matches:
                self._log_file(curr_file, 'OK', f'matches {tmp_file}')
            else:
                self._handle_changed_file(curr_file, template)

    # --------------------
    ## handle missing file by copying template
    #
    # @param curr_file  path to current file
    # @param template   path to template file
    # @return None
    def _handle_missing_file(self, curr_file, template):
        src = template
        dst = curr_file
        # log.dbg(f'{curr_file: <20}: src:{src} dst:{dst}')
        shutil.copyfile(src, dst)

    # --------------------
    ## handle changed file
    #
    # @param curr_file  path to current file
    # @param template   path to template file
    # @return None
    def _handle_changed_file(self, curr_file, template):
        skip_meld = self._check_unimplemented(curr_file, template)
        if skip_meld:
            # files are identical except for one line: cmn_unimplemented
            self._log_file(curr_file, 'OK', 'unimplemented, skipping')
            return

        # files are different, report if they are staged
        checked_out = self._is_git_staged(curr_file)
        if checked_out:
            self._log_file(curr_file, 'CHK', 'does not match; git checked out')
        else:
            self._log_file(curr_file, 'CHK', 'does not match; not git checked out')
        self._check_meld(curr_file, template)

    # --------------------
    ## return if the file is git checked out or git staged
    #
    # @param curr_file  path to current file
    # @return True if file is gie checkout or staged, False otherwise
    def _is_git_staged(self, curr_file):
        out = os.popen(f'git status -s {curr_file}').read()
        out = out.strip()
        return out != ''

    # --------------------
    ## handle checked out file
    #
    # @param curr_file  path to current file
    # @param template   path to template file
    # @return None
    def _check_unimplemented(self, curr_file, template):
        skip_meld = False
        # check if cmn_unimplemented is normal to use
        # in these files only
        check_files = [
            'doit',
            'do_build',
            'do_gen',
            'do_ut',
            'do_ver',
            'do_post_ver',
            'do_publish',
        ]

        if curr_file not in check_files:
            return skip_meld

        diffs = []
        with open(curr_file, 'r', encoding='utf-8') as file1:
            with open(template, 'r', encoding='utf-8') as file2:
                lines1 = file1.readlines()
                lines2 = file2.readlines()

                idx = 0
                for line in lines1:
                    if line != lines2[idx]:
                        # uncomment to delete
                        # log.dbg('diff found:')
                        # log.dbg(f'   curr_file: "{line.strip()}"')
                        # log.dbg(f'   template : "{lines2[idx].strip()}"')
                        diffs.append(line.strip())
                    else:
                        idx += 1

        if len(diffs) == 1:
            if diffs[0].find('cmn_unimplemented') != -1:
                skip_meld = True
        return skip_meld

    # --------------------
    ## handle updating the file from the template
    #
    # @param curr_file  path to current file
    # @param template   path to template file
    # @return None
    def _check_meld(self, curr_file, template):
        if not self._show_meld:
            return

        self._meld_count += 1
        os.system(f'meld {template} {curr_file} &')

    # --------------------
    ## log the results for the given file
    #
    # @param curr_file  path to current file
    # @param tag        "CHK" or "OK"
    # @param line       the line to log
    # @return None
    def _log_file(self, curr_file, tag, line):
        if len(curr_file) <= 20:
            line = f'{tag: <3} {curr_file: <20}: {line}'
        else:
            line = f'{tag: <3} {curr_file: <35}: {line}'

        if tag == 'CHK':
            log.highlight(line)
        else:
            log.line(line)

    # --------------------
    ## handle various files that are in tools/xplat_utils but
    # may have an optional update in tools. If they match, then
    # the optional update can be removed.
    #
    # @return None
    def _handle_common_files(self):
        self._check_for_duplicate('doxyfile_master')
        self._check_for_duplicate('doxyfile_template')
        self._check_for_duplicate('pylint.rc')
        self._check_for_duplicate('ruff.toml')

        path = os.path.join('.idea', '.name')
        if os.path.isfile(path):
            os.remove(path)

    # --------------------
    ## check if the given file is in tools and in tools/xplat_utils.
    # If they match, delete the one in tools.
    #
    # @param fname  the file to check
    # @return None
    def _check_for_duplicate(self, fname):
        path1 = os.path.join('tools', fname)
        if not os.path.isfile(path1):
            return

        path2 = os.path.join('tools', 'xplat_utils', fname)
        matches = filecmp.cmp(path1, path2, shallow=False)
        if matches:
            os.remove(path1)
            log.line(f'{path1: <25} removed, duplicate of {path2}')
        else:
            self._log_file(path1, 'CHK', f'does not match {path2}')
            self._check_meld(path1, path2)

    # --------------------
    ## handle the medver additional files. If one is present
    # then the others should also be prsent. Note the srs.json is optional.
    #
    # @return None
    def _handle_medver_files(self):
        files_exist = [
            os.path.isfile('cfg.json'),
            os.path.isfile('conftest.py'),
        ]
        if not all(files_exist):
            log.line('medver files not found')
            return

        if not os.path.isfile('srs.json'):
            log.warn('medver files found, but srs.json not found. Is it missing?')

        self._handle_check_template('conftest.py', 'conftest_py_template')

    # --------------------
    ## check for other files in the directory.
    # report if they are handled or not, or can be safely ignored
    # by this script.
    #
    # @return None
    def _dev_double_check(self):
        # TODO can .idea files be checked?
        # TODO should tools/loader.py be handled?

        ok_to_skip = [
            '.coverage',
            'cfg.json',  # handled
            'conftest.py',  # handled
            'Doxyfile',
            'Findcpip.cmake',
            'LICENSE.txt',
            'Makefile',
            'MANIFEST.in',
            'README.md',
            'README_template.md',
            'gen.py',
            'todo.md',
            'xplat.cfg',
            'zsubm_branch',
            '__init__.py',
            'requirements.txt',
            'set_cfg.sh',
            'set_env.sh',  # handled
            'setup.py',
            'setup_template.py',
            'srs.json',
            'test_process.md',
            'do_install_macos',
            'do_install_msys2',
            'do_install_ubu',
            'do_subm_install_macos',
            'do_subm_install_ubu',
            'version_info.json',
            'version_info.md',
        ]

        for root, _, files in os.walk('.', topdown=True):
            if root.startswith('./.git'):
                continue
            if root.startswith('./doc'):
                continue
            if root.startswith('./out'):
                continue
            if root.startswith('./venv'):
                continue
            if root.startswith('./cmake-build-debug'):
                continue
            if root.startswith('./cmake-build-release'):
                continue
            if root.startswith('./debug'):
                continue
            if root.startswith('./release'):
                continue
            if root.startswith('./tools/xplat_utils'):
                continue
            if root.startswith('./.idea'):
                continue
            if root.startswith('./dist'):
                continue
            if root.find('__pycache__') != -1:
                continue
            if root.find('.pytest_cache') != -1:
                continue
            if root.find('.egg-info') != -1:
                continue
            if root.startswith('./.ruff_cache'):
                continue

            if root.startswith('./ut'):
                continue
            if root.startswith('./ver'):
                continue
            if root.startswith('./iuv'):  # medver-pytest only
                continue

            if self._repo_type == 'app' and root.startswith('./lib'):  # python
                continue
            if self._repo_type == 'app' and root.startswith('./src'):  # cpp and arduino
                continue

            if self._repo_tech == 'python' and \
                    self._repo_type == 'module' and \
                    root.startswith(f'./{self._repo_dir}/lib'):  # python
                continue

            if self._repo_type == 'module' and root.startswith('./lib'):  # cpp and arduino
                continue
            if self._repo_type == 'module' and root.startswith('./sample'):
                continue

            # repos that do pyinstaller builds
            if self._repo_name in ['find-the-best', 'remote-terminal'] and \
                    root.startswith('./build'):
                continue

            # repo specific
            if self._repo_name == 'pyalamake' and root.startswith('./src'):
                continue
            if self._repo_name == 'cpip-common' and root.startswith('./staging'):
                continue
            if self._repo_name == 'budget-private' and root.startswith('./data'):
                continue

            # log.dbg(f'root:{root} dirs:{dirs} files:{files}')
            for fname in sorted(files):
                path = os.path.join(root, fname)
                if path.startswith('./pf_'):
                    continue
                if self._repo_name == 'budget-private' and path.endswith('.xlsx'):
                    continue

                if fname in self.files_to_check:
                    # log.line(f'ok1    path:{path}')
                    pass
                elif fname in ok_to_skip:
                    # log.line(f'ok2    path:{path}')
                    pass
                else:
                    log.line(f'check *path:{path}')

    # --------------------
    ## abort the session with the given message.
    #
    # @param msg   the message to log
    # @return does not return, exits with a rc=1
    def _abort(self, msg):
        import sys
        log.err(msg)
        sys.exit(1)

    ## the files to check
    files_to_check = {
        # === common across all techs/types
        'do_check': [
            {
                'tech': ['python', 'cpp', 'arduino'], 'type': ['app', 'module'],
                'template': 'do_check_template',
                'repos': {},
            },
        ],
        'do_clean': [
            {
                'tech': ['python', 'cpp', 'arduino'], 'type': ['app', 'module'],
                'template': 'do_clean_template',
                'repos': {},
            },
        ],
        'do_doc': [
            {
                'tech': ['python', 'cpp', 'arduino'], 'type': ['app', 'module'],
                'template': 'do_doc_template',
                'repos': {},
            },
        ],
        'do_env': [
            {
                'tech': ['python', 'cpp', 'arduino'], 'type': ['app', 'module'],
                'template': 'do_env_template',
                'repos': {},
            },
        ],
        'do_install': [
            {
                'tech': ['python', 'cpp', 'arduino'], 'type': ['app', 'module'],
                'template': 'do_install_template',
                'repos': {},
            },
        ],
        'do_lint': [
            {
                'tech': ['python', 'cpp', 'arduino'], 'type': ['app', 'module'],
                'template': 'do_lint_template',
                'repos': {},
            },
        ],
        'do_post_ver': [
            {
                'tech': ['python', 'cpp', 'arduino'], 'type': ['app', 'module'],
                'template': 'do_post_ver_template',
                'repos': {},
            },
        ],
        'do_subm_update': [
            {
                'tech': ['python', 'cpp', 'arduino'], 'type': ['app', 'module'],
                'template': 'do_subm_update_template',
                'repos': {},
            },
        ],
        'do_ver': [
            {
                'tech': ['python', 'cpp', 'arduino'], 'type': ['app', 'module'],
                'template': 'do_ver_template',
                'repos': {'medver-pytest': 'skip'},
            },
        ],
        '.gitignore': [
            {
                'tech': ['python', 'cpp', 'arduino'], 'type': ['app', 'module'],
                'template': 'gitignore_template',
                'repos': {},
            },
        ],
        '.gitmodules': [
            {
                'tech': ['python', 'cpp', 'arduino'], 'type': ['app', 'module'],
                'template': 'gitmodules_template',
                'repos': {},
            },
        ],
        'tools/set_env.sh': [
            {
                'tech': ['python', 'cpp', 'arduino'], 'type': ['app', 'module'],
                'template': 'set_env_sh_template',
                'repos': {},
            },
        ],
        # === install related
        'tools/install/do_install_macos': [
            {
                'tech': ['python'], 'type': ['app'],
                'template': 'do_install_macos_py_app_template',
                'repos': {},
            },
            {
                'tech': ['python'], 'type': ['module'],
                'template': 'do_install_macos_py_mod_template',
                'repos': {},
            },
            {
                'tech': ['cpp'], 'type': ['app'],
                'template': 'do_install_macos_cpp_app_template',
                'repos': {},
            },
            {
                'tech': ['cpp'], 'type': ['module'],
                'template': 'do_install_macos_cpp_mod_template',
                'repos': {},
            },
            {
                'tech': ['arduino'], 'type': ['app'],
                'template': 'do_install_macos_ard_app_template',
                'repos': {},
            },
            {
                'tech': ['arduino'], 'type': ['module'],
                'template': 'do_install_macos_ard_mod_template',
                'repos': {},
            },
        ],
        'tools/install/do_install_msys2': [
            {
                'tech': ['python'], 'type': ['app'],
                'template': 'do_install_msys2_py_app_template',
                'repos': {},
            },
            {
                'tech': ['python'], 'type': ['module'],
                'template': 'do_install_msys2_py_mod_template',
                'repos': {},
            },
            {
                'tech': ['cpp'], 'type': ['app'],
                'template': 'do_install_msys2_cpp_app_template',
                'repos': {},
            },
            {
                'tech': ['cpp'], 'type': ['module'],
                'template': 'do_install_msys2_cpp_mod_template',
                'repos': {},
            },
            {
                'tech': ['arduino'], 'type': ['app'],
                'template': 'do_install_msys2_ard_app_template',
                'repos': {},
            },
            {
                'tech': ['arduino'], 'type': ['module'],
                'template': 'do_install_msys2_ard_mod_template',
                'repos': {},
            },
        ],
        'tools/install/do_install_ubu': [
            {
                'tech': ['python'], 'type': ['app'],
                'template': 'do_install_ubu_py_app_template',
                'repos': {},
            },
            {
                'tech': ['python'], 'type': ['module'],
                'template': 'do_install_ubu_py_mod_template',
                'repos': {},
            },
            {
                'tech': ['cpp'], 'type': ['app'],
                'template': 'do_install_ubu_cpp_app_template',
                'repos': {},
            },
            {
                'tech': ['cpp'], 'type': ['module'],
                'template': 'do_install_ubu_cpp_mod_template',
                'repos': {},
            },
            {
                'tech': ['arduino'], 'type': ['app'],
                'template': 'do_install_ubu_ard_app_template',
                'repos': {},
            },
            {
                'tech': ['arduino'], 'type': ['module'],
                'template': 'do_install_ubu_ard_mod_template',
                'repos': {},
            },
        ],
        'tools/install/do_subm_install_macos': [
            {
                'tech': ['python', 'cpp', 'arduino'], 'type': ['app', 'module'],
                'template': 'do_subm_install_macos_template',
                'repos': {},
            },
        ],
        'tools/install/do_subm_install_ubu': [
            {
                'tech': ['python', 'cpp', 'arduino'], 'type': ['app', 'module'],
                'template': 'do_subm_install_ubu_template',
                'repos': {},
            },
        ],
        # === for modules only
        'do_publish': [
            {
                'tech': ['python'], 'type': ['module'],
                'template': 'do_publish_template',
                'repos': {'xplat-utils-ut': 'include', 'cpip-common': 'skip'},
            },
            {
                'tech': ['cpp'], 'type': ['module'],
                'template': 'do_publish_cpip_template',
                'repos': {'cpip-common': 'include'},
            },
        ],
        # === python only
        'pytest.ini': [
            {
                'tech': ['python'], 'type': ['app', 'module'],
                'template': 'pytest_ini_template',
                'repos': {'pyalamake': 'skip'},
            },
        ],
        'setup.cfg': [
            {
                'template': 'setup_cfg_template',
                'tech': ['python'], 'type': ['app', 'module'],
                'repos': {},
            },
        ],
        # === multiple templates for techs/types
        'do_update': [
            {
                'tech': ['python'], 'type': ['app'],
                'template': 'do_update_pyapp_template',
                'repos': {'pyalamake': 'skip'},
            },
            {
                'tech': ['python'], 'type': ['module'],
                'template': 'do_update_pymod_template',
                'repos': {'pyalamake': 'skip'},
            },
            {
                'tech': ['cpp', 'arduino'], 'type': ['app', 'module'],
                'template': 'do_update_cpp_app_template',
                'repos': {'pyalamake': 'include'},
            },
        ],
        'do_ut': [
            {
                'tech': ['python'], 'type': ['app', 'module'],
                'template': 'do_ut_template',
                'repos': {'pyalamake': 'skip'},
            },
            {
                'tech': ['cpp', 'arduino'], 'type': ['app', 'module'],
                'template': 'do_ut_cpp_app_template',
                'repos': {'pyalamake': 'include'},
            },
        ],
        'doit': [
            {
                'tech': ['python'], 'type': ['app'],
                'template': 'doit_pyapp_template',
                'repos': {'pyalamake': 'skip'},
            },
            {
                'tech': ['python'], 'type': ['module'],
                'template': 'doit_pymod_template',
                'repos': {'pyalamake': 'skip'},
            },
            {
                'tech': ['cpp'], 'type': ['app', 'module'],
                'template': 'doit_cpp_app_template',
                'repos': {'pyalamake': 'include'},
            },
            {
                'tech': ['arduino'], 'type': ['app'],
                'template': 'doit_arduino_app_template',
                'repos': {},
            },
        ],
        # == cpp and arduino only
        'do_gen': [
            {
                'tech': ['cpp', 'arduino'], 'type': ['app', 'module'],
                'template': 'do_gen_template',
                'repos': {'pyalamake': 'include'},
            },
        ],
        'do_build': [
            {
                'tech': ['cpp', 'arduino'], 'type': ['app', 'module'],
                'template': 'do_build_template',
                'repos': {'pyalamake': 'include'},
            },
        ],
        '.clang-tidy': [
            {
                'tech': ['cpp', 'arduino'], 'type': ['app', 'module'],
                'template': 'clang-tidy-template',
                'repos': {'pyalamake': 'include'},
            },
        ],
        '.clang-format': [
            {
                'tech': ['cpp', 'arduino'], 'type': ['app', 'module'],
                'template': 'clang-format-template',
                'repos': {'pyalamake': 'include'},
            },
        ],
        # == arduino only
        'do_upload': [
            {
                'tech': ['arduino'], 'type': ['app'],
                'template': 'do_upload_template',
                'repos': {'pyalamake': 'include'},
            },
        ],
    }
