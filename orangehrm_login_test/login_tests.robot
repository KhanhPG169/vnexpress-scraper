*** Settings ***
Library    SeleniumLibrary

*** Variables ***
${URL}     https://opensource-demo.orangehrmlive.com/web/index.php/auth/login
${VALID_USERNAME}    Admin
${VALID_PASSWORD}    admin123
${INVALID_USERNAME}  wronguser
${INVALID_PASSWORD}  wrongpass

*** Test Cases ***

Valid Login Should Succeed
    Open Browser    ${URL}    chrome
    Maximize Browser Window
    Input Text    name=username    ${VALID_USERNAME}
    Input Text    name=password    ${VALID_PASSWORD}
    Click Button    xpath=//button[@type='submit']
    Wait Until Page Contains Element    xpath=//span[text()='Dashboard']    timeout=10s
    [Teardown]    Close Browser

Invalid Login Should Fail
    Open Browser    ${URL}    chrome
    Maximize Browser Window
    Input Text    name=username    ${INVALID_USERNAME}
    Input Text    name=password    ${INVALID_PASSWORD}
    Click Button    xpath=//button[@type='submit']
    Wait Until Page Contains    Invalid credentials    timeout=5s
    [Teardown]    Close Browser
