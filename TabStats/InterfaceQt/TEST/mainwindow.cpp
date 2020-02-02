#include "mainwindow.h"
#include "ui_mainwindow.h"

// CONSTRUCTOR
MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    exe_path = "../../LogicPythonCompiled/dist/ScriptTabStats.exe";  // FOR PROD
    //exe_path = "C:/Users/Charly/CloudStation/Projets/Perso/Tab_Stat_Employes/Executable/LogicPythonCompiled/dist/ScriptTabStats.exe";  // FOR TESTS

    // TO DO NOT HAVE TO COMPILE, TEST DIRECTLY ON SCRIPT
    //exe_path = "C:/Users/Charly/CloudStation/Projets/Perso/Tab_Stat_Employes/Executable/LogicPythonCompiled/ScriptTabStats.py"; // FOR TESTS

    file_path = "";

    // THE SCRIPT NEED A PATH, SO DO NOT SET TO TRUE FOR TESTS
    existingDir = false;

}


// DESTRUCTOR
MainWindow::~MainWindow()
{
    delete ui;
}

// LEAVE THE APPLICATION
void MainWindow::on_pushButton_quit_clicked()
{
    QApplication::quit();
}

// CHOOSE THE DIRECTORY WHERE THERE IS THE DATA FILE ".xlsx" TO ANALYSE
void MainWindow::on_pushButton_choiceFile_clicked()
{
    file_path = QFileDialog::getExistingDirectory(this, "Choisissez le dossier où se trouve le fichier de données avec l'extension '.xlsx'.", "C://", QFileDialog::ShowDirsOnly);
    if (file_path!= "" ){
        existingDir = true;
    }
}


// START PYTHON SCRIPT FOR CALCUL
 void MainWindow::on_pushButton_validate_clicked()
{

     // COMMENT FOR TESTS

     if (existingDir == true){


         QString employesDesires = ui->employesDesiresLineEdit->text();
         QProcess *python = new QProcess(this);

         QStringList arguments {employesDesires, file_path};
         python->start(exe_path, arguments);
         //python->start(exe_path);

         // TO DO NOT HAVE TO COMPILE, TEST DIRECTLY ON SCRIPT
         //QStringList arguments {exe_path, employesDesires, file_path};
         //python->start("Python", arguments);


         if (python->waitForStarted(-1)){
            python->waitForFinished();
            python->close();
            QMessageBox::information(this, "No errors",  "Script was executed.");

         } else {
             QMessageBox::information(this, "Error",  "Script does not started, contact the developper");
         }

         delete python;
         python = nullptr;

     } else {
         QMessageBox::information(this, "Error", "Any folder have been selected.");

     }


}
