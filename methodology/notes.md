# 测试工作笔记：

#### 1、移动端

移动端-CPU\GPU\内存、流量、电量、启动和切换响应时间、渲染帧率\刷新率Fps、数据缓存（修改、类似）压力/负载-特定区域流量、最大连接数/storage、反复大get请求、大文件下载、反复大post写入；响应时间、硬件限制（CPU\RAM\IO)、吞吐量TPS、打开数据库连接、第三方内容

#### 全覆盖、兼容、网络、升级、权限过期

adb shell dumpsys connectivity // 查看连接情况
adb shell dumpsys package com.yude.jieyao
adb shell am start com.viide.repair/.MainActivity filter eafbc70
adb shell am start  com.android.settings/com.android.settings.Settings
adb pull /data/data/... C:\Users\EDY\Desktop
adb shell pm list packages -3

#### 压力测试

Jmeter 对接口  
Monkey对APP 进行压力测试。（正常、crash、ANR）   
     adb  shell  monkey –p  sogou.mobile.explorer  –v 1000 

### 2、自动化测试框架

#### rest-assured+allure+testNg，requests+pytest+allure（采用），postman+Newman，robotframework,
![](.notes_images/ec201a28.png)     
数据驱动（高级参数化区别）、关键字驱动（动作级）、page object model、Python-重构自动化-数据驱动

pipline-拉代码、本地搭环境、本地运行服务、启动脚本代码、保存报告、mock服务
![](.notes_images/5f2d8c36.png)
   
测试服务器（本地、线上）；   

自动化测试服务器、性能测试服务器；

代码上线流程工具（上传Git、打包编译、sonar、smoke、发布stage测试环境）；

Python JSON库：         
![](.notes_images/876a2873.png)

gradle
docker

##### 记录一些自动化测试框架的笔记：
###### Python版本
</br>一、unittest——单元测试
特点：测试用例的组织；适合中小型项目。
</br>二、pytest——单元测试、功能测试、集成测试
<特点：功能完善灵活；插件丰富
</br>三、nose2——单元测试
特点：自动发现和运行；与unittest兼容
</br>四、Robot Framework——接受测试、回归测试、行为驱动开发（BDD）
特点：关键字驱动；丰富的库和工具；适合大型项目
</br>五、 Selenium——WEB测试、回归测试
特点：兼容多浏览器、操作系统、测试框架、编程语言；适用跨浏览器和web交互项目
</br>六、Behave——行为驱动开发（BDD）、接受测试
特点：自然语言（Gherkin）编写测试用例；支持场景和步骤定义
</br>七、Lettuce——行为驱动开发（BDD）、接受测试
特点：支持自然语言（Gherkin）编写测试用例；轻量级
</br>八、locust——负载测试、性能测试
特点：使用Python编写行为脚本；支持分布式模拟大量用户
</br>九、pytest-django——Django项目的单元测试、功能测试
特点：支持测试数据库、视图和模板
</br>十、Jenkins——CI/CD工具
特点：支持多种插件和框架；用于构建流水线项目

###### JAVA版本
</br>一、Junit——单元测试
特点：轻量级，支持测试驱动开发（TDD）和行为驱动开发（BDD）
</br>二、TestNG——单元测试、集成测试
特点：功能强大，支持参数化测试、依赖测试和组合测试等复杂场景
</br>三、Selenium——功能测试、回归测试、UI测试
特点：适用于WEB多浏览器
</br>四、Appium——功能测试、回归测试
特点：支持iOS、Android原生应用、混合应用和移动Web应用的自动化测试，提供丰富的API
</br>五、Cucumber——行为驱动开发（BDD）、验收测试
特点：支持BDD，Gherkin语言描述测试用例，支持集成JUnit或TestNG执行
</br>六、RestAssured——功能测试、集成测试
特点：用于REST API测试，支持验证响应
同类：HttpClient
</br>七、Mockito——Mocking框架
特点：创建和配置mock对象
同类的有WireMock
</br>八、Hamcrest——断言库
特点：丰富的匹配器，易于维护
</br>九、Jenkins——CI\CD工具
特点：流水线构建
</br>十、JMeter——性能测试、负载测试特点：多场景多用户
</br>AI版本
</br>一、测试用例生成
生成代码变种、自动调参
</br>二、特定框架和工具
1、test.ai——识别和测试用户界面元素；用于UI测试
2、DeepCode——分析代码发现代码质量问题；用于代码审查和静态代码分析
3、Applitools——视觉测试解决方案，用户界面回归测试；UI/UX测试，适合复杂的WEB和移动应用
</br>三、数据驱动测试
自动数据生成和变异；生成多样化测试数据：图像、文本和音频；适用于图像分类、自然语言处理和语音识别
</br>四、模拟和仿真
AI模拟平台；自动驾驶、机器人等
</br>五、自动化评估和报告
1、智能日志分析，适用分布式系统和微服务架构的日志分析
2、自动化报告生成，
###### 其他框架工具
Puppeteer 和 Jest 经常一起使用，可以实现强大的端到端测试，测试react程序。
Puppeteer 提供了浏览器自动化能力,负责模拟用户操作。是一个 Headless Chrome Node API，它控制 Chrome 浏览器的版本。
</br>Jest 提供了测试框架，负责组织和运行测试用例。 



### 3、其他

#### 项目管理

工作规范文档化，流程化   

#### 质量认证体系
[CMMI(初始级、已管理级、已定义级、量化管理级、优化级)](https://cmmiinstitute.com/pars/?StateId=caf45928-cb61-4547-ac60-4b028a2712c7)      
[SEI美国软件工程学会(software engineering institue,简称SEI)](https://www.sei.cmu.edu/about/index.cfm)   
[ISO20000信息技术服务管理体系\ISO27001信息安全管理体系\ISO9001质量管理体系](https://www.cqc.com.cn/www/chinese/txrz/)       
1、ISO 9001：ISO 9001是一项国际标准，用于质量管理体系。它为组织提供了建立和维护质量管理体系的指南，包括软件开发组织。通过实施ISO 9001，组织可以确保其软件开发过程符合国际认可的质量标准。
   
2、CMMI（Capability Maturity Model Integration）：CMMI是一种过程改进方法，旨在评估和改进组织的软件开发过程。它定义了一系列成熟度级别和关联的过程领域，帮助组织了解其软件开发能力，并提供改进路径。CMMI的级别包括初始级别、被管理级别、定义级别、量化管理级别和优化级别。
   
3、IEEE 730：IEEE 730是软件质量保证计划的标准，它描述了在软件开发生命周期中执行的质量保证活动。该标准包括质量目标、质量保证活动、质量标准和审查过程等方面。
   
4、IEEE 829：IEEE 829是软件测试文档的标准，定义了软件测试过程中的各种文档类型和内容。这些文档包括测试计划、测试设计规范、测试用例、缺陷报告等，有助于确保测试过程的可追溯性和一致性。
   
5、Six Sigma：Six Sigma是一种质量管理方法，旨在减少产品或过程的缺陷率。它基于数据驱动的方法，使用统计工具和质量技术来分析和改进过程。通过应用Six Sigma，组织可以降低软件开发过程中的缺陷率，提高产品质量。
#### 合约

NFT智能合约特性，remix，B-智能合约测试-solidity测试框架；nodejs本地搭链，发布合约

#### 线上服务监控

### 混沌测试

### 4、一些工具

[plantUML](https://plantuml.com/zh/starting)（时序图、用例图、类图、组件图、部署图、状态图、框架图、甘特图……）
[docker](https://www.coonote.com/docker/docker-common-commands.html)——搭建服务和测试运行环境    

selenium（后端）/cypress(前端)   
gradle
testNG   


### 5、经验累积

1. UI自动化
   规范类：对齐、大小写、标点符号、中英文字体等；
   提示类：错误提示
   输入类：正常值、边界值、错误值、null、不输入、异常类型、sql语句
   #### 框架：
   Selenium：Selenium是最受欢迎的UI自动化测试框架之一，支持多种编程语言，如Java、Python和C#。它可以模拟用户在网页上的操作，执行各种测试任务。   
   Appium：Appium是一个开源的UI自动化测试框架，专门用于移动应用程序的测试。它支持多种移动平台，如iOS和Android，并提供跨平台的测试能力。   
   Cypress：Cypress是一个现代化的JavaScript前端测试框架，旨在对Web应用程序进行端到端的自动化测试。它具有简单易用的API和强大的调试功能。   
   TestComplete：TestComplete是一款功能强大的UI自动化测试工具，支持多种应用程序类型，包括Web、桌面和移动应用程序。它提供了丰富的测试功能和易于使用的脚本记录功能。   
   [Maestro](https://maestro.mobile.dev/)：


3. 接口自动化
   数据驱动&过程驱动
   接口自动化筛选标准   
   接口请求耗时：不保持连接>保持连接，requests=httpx(同步模式)>httpx(异步模式)>aiohttp   
4. 精准测试
5. 单元测试
   Junit、TestNG、
6. TDD（测试驱动开发）
7. BDD（行为驱动开发）：契约测试
8. DevOPS
9. ![](.notes_images/27999197.png)POM(page object model)

### 关于敏捷的一些信息
##### [Spotify敏捷模式三部曲](https://www.leangoo.com/14003.html)
##### 四种流行的敏捷开发方法：Scrum、Kanban、Lean和XP

