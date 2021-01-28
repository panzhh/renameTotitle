#!/usr/bin/python
import sys
import os
import subprocess


def copyAndRename(file_name):
    command = "pdftitle -p " + file_name
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p_status = p.wait()

    if p_status < 0:
        print("could not open %s" % file_name)

    new_file_name = output.decode('utf-8').replace(" ", "_").replace("\n", "") + ".pdf"

    if os.path.exists(new_file_name):
        ### new_file_name already exists, so we don't re-create.
        return

    q = subprocess.Popen("cp %s %s" % (file_name, new_file_name), stdout=subprocess.PIPE, shell=True)
    (output, err) = q.communicate()
    q_status = q.wait()

    if q_status < 0:
        print("could not copy file %s" % file_name)
        return

    print("copy %s to %s is done." % (file_name, new_file_name))

if __name__ == "__main__":
    dir_path = os.path.dirname(os.path.realpath(__file__))
    assert len(sys.argv) == 2, "please specify the pdf file or directory."
    for i, arg in enumerate(sys.argv):
        if i == 0:
            continue

        if os.path.isabs(arg):
            file_name = arg
        else:
            file_name = dir_path + "/" + arg

        if not os.path.exists(file_name):
            print("%s does not exit" % file_name)
            continue

        if os.path.isdir(file_name):
            files = [f for f in os.listdir(file_name) if os.path.isfile(f)]
            files = filter(lambda f: f.endswith(('.pdf', '.PDF')), files)

            for f in files:
                copyAndRename(f)
        else:
            copyAndRename(file_name)

