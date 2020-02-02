#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QMessageBox>
#include <QFileDialog>
#include <QProcess>


namespace Ui {
    class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = nullptr);
    ~MainWindow();


private slots:
    void on_pushButton_quit_clicked();

    void on_pushButton_validate_clicked();

    void on_pushButton_choiceFile_clicked();

private:
    Ui::MainWindow *ui;
    QString file_path;
    QString exe_path;
    //QProcess python;
    bool existingDir;
};


#endif // MAINWINDOW_H
