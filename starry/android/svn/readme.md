svn.txt文件

第一行 SVN代码地址

第二行 检出到指定名称的文件夹

第三行 需要打包的项目根目录


Android编译时需要配置SDK和NDK环境变量，脚本采用读取evn.txt的方式配置环境变量

evn.txt文件

第一行 SDK

第二行 NDK


不配置环境变量打包会出现如下错误

#### SDK location not found.
Define location with sdk.dir in the local.properties file or with an ANDROID_HOME environment variable.

设置ANDROID_HOME in terminal
```
echo 'export ANDROID_HOME=/xxx/Sdk' >> ~/.bashrc
echo 'export PATH=$PATH:$ANDROID_HOME' >> ~/.bashrc
source ~/.bashrc
```

#### NDK not configured.
Download the NDK from http://developer.android.com/tools/sdk/ndk/.Then add ndk.dir=path/to/ndk in local.properties

设置ANDROID_NDK_HOME in terminal
```
echo 'export ANDROID_NDK_HOME=/xxx/android-ndk-xxx' >> ~/.bashrc
echo 'export PATH=$PATH:$ANDROID_NDK_HOME' >> ~/.bashrc
source