#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2019+ Gradiant, Vigo, Spain

from bob.gradiant.face.databases.classes import ClassExample


def main():
    class_example = ClassExample()
    print(class_example.get_greetings())


if __name__ == '__main__':
    main()
