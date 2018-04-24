# Anaconda Notebooks in Digital Exam rooms

##### Abstract

Early 2018, Anaconda Python 3.6 has been installed on the exam computers in IWO. 
Next to the TestVision exams, students can use a notebook during the exam, similarly to using a scientific calculator. Using an interactive notebook during exams yields a far more natural test of the students capacities and makes it possible to ask deeper questions involving real life datasets. 
In this short note we describe three ways in which the notebooks can be used during exams. Links to additional material are provided as well.

#### Notebook exam github account
All information on the notebook exams can be found at <https://github.com/UvA-FNWI/notebook-exams>.

#### Using notebooks during exams

We describe three ways in which the notebooks can be used during exams. First, as a device next to a TestVision exam, where students hand in a TestVision exam. In the other two cases, the student hands in the notebook itself.

###### Technical setup
In all three cases, the students interact with both TestVision and with a Jupyter notebook environment. The students have two icons on their desktop with which they can start these two applications. 

Similar to Testvision, the data in the notebook environment is hidden to the students, until the instructor releases it (for all simultaneously).

Typically, the exam consists of a TestVision exam, a notebook with exam material and additional datasets.


##### Notebook next to a TestVision exam

* All answers are entered in TestVision, and exams are graded in TestVision.
* The notebook is used as an instrument to obtain the answers. 
* In this case the notebook is best viewed as an assistant to the student making the exam, comparable to a combination of a calculator, scrap paper, and a manual.
* It is possible to let the student upload the notebook in the TestVision exam.

##### The notebook is the exam

* The notebook contains all questions and material, like in an assignment.
* The students interacts during the exam only with the notebook.
* TestVision is only used to safely collect the notebooks: the exam consists of one question, in which the students uploads her notebook.

###### Version 1

* Notebooks are manually graded without any assistance.

###### Version 2: using [NBgrader](http://nbgrader.readthedocs.io/en/stable)

* Notebooks are created using [NBgrader](http://nbgrader.readthedocs.io/en/stable)
* This has some extra initial investment (learning NBgrader, and keeping to its rather restricted format), but pays of with 
	* 	autograded questions (by unit tests)
	* handy manual grading inside the notebook
* Each question can either be auto or manually graded. After auto-grading, it is easy to override the autograde. Autograding goes via unit-tests. Typically one asks to compute the value of a certain variable or to define a function.
* Manual grading can only be done "by student" (not by question), but works smoothly. The grader enters the grade in a special grade box attached to the cell of the answer. The maximum number of points is indicated, and extra bonus points can be given too. 
* All data about grading is stored in an intricate SQL lite database, but is easily exported to a spreadsheet with schema: `student id; question id; regular points; extra points`, allowing for quick calculations of the final grades, kappa measures and easy adjustments, weightings, etc.

###### NBgrader How to 
A detailed step by step plan for the NBgrader setup is available at <https://github.com/UvA-FNWI/notebook-exams/blob/master/Using_notebooks_for_exams/Using_nbgrader/nbgrader_workflow.ipynb>. This plan describes all steps, from creating the exam (starting from a template-example), creating the student version, getting it on the IWO computers, collecting the exams and putting them in the nbgrading system, auto and manual grading and finally computing the grades and publishing them in Blackboard/Canvas.





