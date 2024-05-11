<style>
.center {
  display: block;
  margin-left: auto;
  margin-right: auto;
  width: 50%;
}
.aligncenter {
  text-align: center;
}
</style>
Python scripts, solved problems and small projects.

# Operating Systems (OS) Algorithms
Page swapping and scheduling processor work. Including process generator and saving results to files.
- processor scheduling includes: SJF (Shortest Job First), Round Robin (executing processes in time quantum), FCFS (First Come First Serve), LCFS (Last Come First Serve)
- pages swapping includes: LRU (Least Recently Used), FIFO (First Come First Serve)

# Scraper
Web scraper directed into scrapping from job board (pracuj.pl).
- simple GUI
- scraps data from specified source and can store it in .csv file
- can read data from files
- plots results in histogram
- multiple scrapped data can be shown and compared on a single chart
- GUI:

<img src="/Scraper/scraper gui.jpg" alt="gui" title="gui" height="500" class="center">

- Compared results:

<img src="/Scraper/scraper histogram.jpg" alt="histogram" title="histogram" height=50%>

# Huffman compression
Compress files using Huffman algorithm.
- compress files using Huffman algorithm
- reduces file size
- provides encryption and decryption
- note: not (yet) well optimized

# Cryptography
Hides text in image by setting parity of the pixels. Provides some level of steganography because doesn't change every pixel - only if needed. 
- uses provided graphics to hide the text in a pixel value parity
- let's to read hidden text from an image

# AES encoding and decoding
- encoding and decoding files using AES algorithm with external key
