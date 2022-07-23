# **EvaSIM** Installation Instructions
 
![](https://github.com/midiacom/eva-robot/blob/master/Assembly%20Process/capa_form_evasim.png)

In order to facilitate the use of EvaSIM, we managed to package the software with all its dependencies, without having to download and install Python modules. We did it in two versions, one for Windows and one for Linux. To run EvaSIM we recommend **Windows 10** and Linux distributions **Ubuntu 20.04.4** and Linux **Mint 20.3**.
 
1. First, you should download the correct version for your system.
 
    * **EvaSIM (Windows Version):** [EvaSIM-Windows.zip](https://drive.google.com/file/d/1DFTOngK1Vx59LI5tpZ7ynI98ocw5uj0h/view?usp=sharing?target=_blank)

 
    * **EvaSIM (Linux Version):** [EvaSIM-Linux.zip](https://drive.google.com/file/d/1XKnf_R5617iB0tA4-S1uQO62Fcj76AA3/view?usp=sharing?target=_blank)

 
    After downloading the zip file, you should unzip it.
 
    So, you will see an "*eva_sim*" folder. 
 
    Enter the "*eva_sim*" folder and double-click on the "*eva_sim.exe*" file, in the case of the Windows version, or the "*eva_sim*" file, in the case of the Linux version.
 
    Now, **activate** the simulator using the EvaSIM **"Power On"** button, as shown in the next figure.
    ![](https://github.com/midiacom/eva-robot/blob/master/Assembly%20Process/pow_img.png)
 
    If you hear a greeting, everything should be working correctly!

 
`In the Linux version, if after two clicks on "eva_sim" file the simulator does not run, please check if the file has permission to be executed. This can be done by clicking with the right mouse button on the file, selecting the properties option and in the permissions tab activating the option "allow the execution of the file". This can also be done via the command line as follows:`
```
sudo chmod +x eva_sim
```
`In case the previous versions didn't work, or you use a linux based RPM package, as in the case of the Fedora distribution, you can try to install the modules through the terminal and run the simulator using the source code. The source code, also in two flavors, is available through this link:`
[https://github.com/midiacom/eva-robot/tree/master/EvaML-EvaSIM source code](https://github.com/midiacom/eva-robot/tree/master/EvaML-EvaSIM%20source%20code)

** You should use this [document](https://github.com/midiacom/eva-robot/blob/master/EvaSIM%20Testing%20Version/EvaSIM%20-%20Installing%20Instructions%20-%20Appendix%20A.pdf
) with installation instructions.