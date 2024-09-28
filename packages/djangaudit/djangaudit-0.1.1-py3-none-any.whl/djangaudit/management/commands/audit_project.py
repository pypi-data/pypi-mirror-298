import os
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.translation import gettext as _

from djangaudit.lib import (
    find_large_python_files,
    find_non_empty_init_files,
    line_length_counter,
    get_dependencies_version_diffs,
)


class Command(BaseCommand):
    help = _('Basic check of the Django project health')

    def handle(self, *args, **kwargs):
        report = {
            'total_large_files': 0,
            'use_of_init_files': False,
            'total_minor_version_diffs': 0,
            'total_major_version_diffs': 0,
        }
        self.stdout.write(self.style.SUCCESS(f'Checking the Django project health...'))

        # Large files checker
        self.stdout.write(self.style.WARNING('#1 - Checking for large Python files...'))
        large_files = find_large_python_files(settings.BASE_DIR, min_lines=settings.AUDIT_MAX_LINES_PER_FILE)
        if large_files:
            for file_path, num_lines in large_files:
                self.stdout.write(self.style.ERROR(f'{file_path} : {num_lines} lines'))
            report['total_large_files'] = len(large_files)
            self.stdout.write(self.style.ERROR(f'Number of files found: {len(large_files)}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'No Python file with more than 300 lines found in the given directory.'))

        # __init__.py files checker
        self.stdout.write(self.style.WARNING('#2 - Checking for __init__.py files with code...'))
        init_files_with_code = find_non_empty_init_files(settings.BASE_DIR)
        if init_files_with_code:
            for file_path in init_files_with_code:
                self.stdout.write(self.style.SUCCESS(f'{file_path} contains code'))
            report['use_of_init_files'] = True
        else:
            self.stdout.write(self.style.ERROR(f'No __init__.py file containing code found in the given directory.'))

        # Line length checker
        self.stdout.write(self.style.WARNING('#3 - Checking for line length...'))
        line_report = line_length_counter(settings.BASE_DIR)
        report = {**report, **line_report}
        self.stdout.write(self.style.SUCCESS(f'Number of lines less than 80 characters: {report["less_than_80"]}'))
        self.stdout.write(self.style.SUCCESS(f'Number of lines between 80 and 99 characters: {report["between_80_and_99"]}'))
        self.stdout.write(self.style.WARNING(f'Number of lines between 100 and 119 characters: {report["between_100_and_119"]}'))
        self.stdout.write(self.style.ERROR(f'Number of lines more than 120 characters: {report["more_than_120"]}'))

        # Dependencies versions checker
        self.stdout.write(self.style.WARNING('#4 - Checking for dependencies versions...'))
        diff_versions = get_dependencies_version_diffs()
        for package_versions in diff_versions.get('minor', {}):
            self.stdout.write(self.style.WARNING(f'{package_versions} has a minor version difference'))
        report['total_minor_version_diffs'] = len(diff_versions.get('minor', {}))
        for package_versions in diff_versions.get('major', {}):
            self.stdout.write(self.style.ERROR(f'{package_versions} has a major version difference'))
        report['total_major_version_diffs'] = len(diff_versions.get('major', {}))

        # Display the final report
        self.stdout.write(self.style.SUCCESS(f'--- Django project health report ---'))
        self.stdout.write(self.style.SUCCESS(f'Total number of large files: {report["total_large_files"]}'))
        self.stdout.write(self.style.SUCCESS(f'Use of __init__.py files: {report["use_of_init_files"]}'))
        self.stdout.write(self.style.SUCCESS(f'Number of lines less than 80 characters: {report["less_than_80"]}'))
        self.stdout.write(self.style.SUCCESS(f'Number of lines between 80 and 99 characters: {report["between_80_and_99"]}'))
        self.stdout.write(self.style.WARNING(f'Number of lines between 100 and 119 characters: {report["between_100_and_119"]}'))
        self.stdout.write(self.style.ERROR(f'Number of lines more than 120 characters: {report["more_than_120"]}'))
        self.stdout.write(self.style.WARNING(f'Total number of minor version differences: {report["total_minor_version_diffs"]}'))
        self.stdout.write(self.style.ERROR(f'Total number of major version differences: {report["total_major_version_diffs"]}'))
        self.stdout.write(self.style.SUCCESS(f'--- End of report ---'))
