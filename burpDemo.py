import sys
import payloads

def printHelpExit():
    print("burpDemo.py -if <burp-input-file> -p <payload-file> -of <burp-output-file>\n\nNote: please export raw req with burp option !COPY TO FILE!\n")
    exit(-1)

def main():
    args = sys.argv


    inputFile = ""
    outputFile = ""
    payloadFile = ""

    i = 0
    while i < len(args):
        if args[i] == "-p" and len(args) > i+1:
            payloadFile = args[i+1]
            i += 2
            continue
        if args[i] == "-if" and len(args) > i+1:
            inputFile = args[i+1]
            i += 2
            continue
        if args[i] == "-of" and len(args) > i+1:
            outputFile = args[i+1]
            i += 2
            continue
        i += 1

    if inputFile == "" or payloadFile=="" or outputFile == "":
        printHelpExit()
    

    inputFileStream = open(inputFile, "rb")
    payloadFileStream = open(payloadFile, "rb")

    reqData = inputFileStream.read()
    payload = payloadFileStream.read()

    inputFileStream.close()
    payloadFileStream.close()


    pngFileBytes = payloads.FilePayloadAdvanced.pngPLTE.make(payload)


    outputFileStream = open(outputFile, "wb")

    i0 = reqData.find(b"\r\nContent-Type: multipart/form-data; boundary=")
    i1 = reqData.find(b"\r\n",i0+2)
    boundary = reqData[i0+46:i1]

    ibody = reqData.find(b"\r\n\r\n")+4


    i0 = reqData.find(b"\r\n--"+boundary,ibody-2)
    istartFile = -1
    while i0 != -1:
        l0 = reqData.find(b"\r\n", i0+1)
        l1 = reqData.find(b"\r\n", l0+1)
        l2 = reqData.find(b"\r\n", l1+1)
        print(reqData[l1:l2])
        if reqData[l1:l2].startswith(b"\r\nContent-Type: "):
            istartType = l1+16
            iendType = l2

            _type = reqData[istartType:iendType]
            if _type != b"image/png": None # implement some check?

            istartFile = reqData.find(b"\r\n\r\n",l2)+4
            break
        i0 = reqData.find(b"\r\n--"+boundary, i0+1)
    
    if i0 == -1:
        print("'\\r\\nContent-Type: image/png' not found in request")


    istartFile = istartFile
    iEndFile = reqData.find(b"\r\n--"+boundary, istartFile)

    # oldPngFile = reqData[istartFile:iendFile]

    newReqData = reqData[:istartType] + _type + reqData[iendType:istartFile] + pngFileBytes + reqData[iEndFile:]



    outputFileStream.write(newReqData)

if __name__ == "__main__":
    main()