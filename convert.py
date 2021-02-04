import sys
import time

file_bit = sys.argv[1]
file_name = sys.argv[2]
result = ""
add_memory_check = 0
memory_line = 0
memory_size = 0

if len(sys.argv) != 3:
    print("--32bit / --64bit + [file path]")
    sys.exit()

def middle_text_size(text, buf):
    buf = buf.split(text, 1)[1]
    buf = buf.split(";", 1)[0]

    return buf

def add_memory_32(name, size):
    global result
    global add_memory_check
    global memory_size
    global memory_line

    if add_memory_check == 0:
        result += "    |   4   |   4   |   4   |   4   |\n"
        add_memory_check += 1
    if(memory_size == memory_line):
        if(memory_line == 0):
            result += hex(memory_line) + " |"
            memory_line += 0x10
        else:
            result += hex(memory_line) + "|"
            memory_line += 0x10

    print(str(size))
    if(size == 8):
        space_size = len("               ") - len(name)
        result += "     " + name + " "*(space_size-5) + "|"
        memory_size += 0x8
        if(memory_size == 0x10):
            result += "\n"
    elif(size == 4):
        space_size = len("       ") - len(name)
        result += " " + name + " "*(space_size-1) + "|"
        memory_size += 0x4
        if(memory_size == 0x10):
            result += "\n"

    '''
    elif(size == 8):
        space_size = len("               ") - len(name)
        result += "     " + name + " "*(space_size-5) + "|"
        memory_size += 0x8
        if(memory_size == 0x10):
            result += "\n"
        print(str(result))
    
    elif(size > 4):
        if memory_size < size:
            out_line = size / 4
        elif memory_size > size:
            out_line = memory_size - size
    '''
        

def check_variable_size_32(buf):
    if buf.find("[") == -1:
        if "*" in buf:
            buf = middle_text_size("*", buf)
            return 4, buf
        elif buf.find("char") == 1:
            buf = middle_text_size("char ", buf)
            return 1, buf
        elif buf.find("bool") == 1:
            buf = middle_text_size("bool ", buf)
            return 1, buf
        elif buf.find("__int8") == 1:
            buf = middle_text_size("__int8 ", buf)
            return 1, buf
        elif buf.find("__int16") == 1:
            buf = middle_text_size("__int16 ", buf)
            return 2, buf
        elif buf.find("wchar_t") == 1:
            buf = middle_text_size("wchar_t ", buf)
            return 2, buf
        elif buf.find("__int32") == 1:
            buf = middle_text_size("__int32 ", buf)
            return 4, buf
        elif buf.find("int") == 1:
            buf = middle_text_size("int ", buf)
            return 4, buf
        elif buf.find("unsigned int") == 1:
            buf = middle_text_size("unsigned int ", buf)
            return 4, buf
        elif buf.find("long") == 1:
            buf = middle_text_size("long ", buf)
            return 4, buf
        elif buf.find("unsigned long") == 1:
            buf = middle_text_size("unsigned long ", buf)
            return 4, buf
        elif buf.find("size_t") == 1:
            buf = middle_text_size("size_t ", buf)
            return 4, buf
        elif buf.find("__int64") == 1:
            buf = middle_text_size("__int64 ", buf)
            return 8, buf
        elif buf.find("longlong") == 1:
            buf = middle_text_size("longlong ", buf)
            return 8, buf
    else:
        size = buf.split("[", 1)[1]
        size = size.split("]", 1)[0]
        buf = buf.split("char ", 1)[1]
        buf = buf.split("[", 1)[0]
        return int(size), buf

def bit32_run():
    f = open(file_name, 'r')
    buf = f.readline()
    if buf.find("struct") != -1:
        struct_name = buf.replace("struct ", "").replace("{","")
        while(1):
            buf = f.readline()
            buf = buf.rstrip("\n")
            if buf == "}":
                print(str(result))
                print("Done")
                break;
            size, variable_name = check_variable_size_32(buf)
            add_memory_32(variable_name, size)
            #print(str(size) + " " + str(variable_name))
        

    else:
        print("Struct Name NOT FOUND")

if __name__ == "__main__":

    if file_bit != "--32bit" and file_bit != "--64bit":
        print("--32bit / --64bit + [file path]")
        sys.exit()
    elif file_bit == "--32bit":
        bit32_run()



