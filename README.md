# NullInjectionUploadScript
NullInjectionUploadScript is a tool to automate null injection attack on file upload endpoint. It supports both generation of file (zip) and auto-exploit for endpoints



# ideas

 - make payload of legitimate jpg file and set (php or other format) payload in metadata. Check if works, check if passes file integrity checks.
 - make payload of legitimate jpg file and set (php or other format) payload in data section so it doesn't fully corrupts image. Check if works, check if passes file integrity checks.
 - same as above for .gif,.png,.pdf
 - add list of extention (name it e.g. extentionFamily): .phar,.php,.php5,.php3,.php7 ...
 - 
