"""
   Description: This script does an accounting of allocated buffers to determine if all buffers fill
      Dictionary omx_output_buffer_handles must have all buffer handles included and logfile_path must point to the log file.
   Author: Doug Nintzel / Intel corporation
"""
logfile_path = "39-main.log_2019_7_24_23_54_2.truncated"
ALLOCATED = True
NOT_ALLOCATED = False

# Below is dictionary of buffer ids from the log being parsed (logfile_path) with format: "'buffername':<allocated> "
omx_output_buffer_handles = {
   '0xf2321f50':NOT_ALLOCATED,
   '0xf2321fa0':NOT_ALLOCATED,
   '0xf2321dc0':NOT_ALLOCATED,
   '0xf2321e60':NOT_ALLOCATED,
   '0xf2321e10':NOT_ALLOCATED,
   '0xf2321f00':NOT_ALLOCATED,
   '0xf1f11960':NOT_ALLOCATED,
   '0xf1f11910':NOT_ALLOCATED,
}
omx_output_buffer_count = len(omx_output_buffer_handles.keys())
print('Log file name {}'.format(logfile_path))
print('omx_output_buffer_count {}'.format(omx_output_buffer_count))
allocated_count = 0

#------------------------------------------------------
# process_logfile_message
#    Look for any of the listed buffer in log message and 
#    Determine if it is empty (FillThisBuffer) or full (FillBufferDone) 
#------------------------------------------------------
def process_logfile_message(logfile_message):
    global allocated_count
    for buffer_id in omx_output_buffer_handles.keys():
        if buffer_id in logfile_message:
           # Framework is giving codec empty buffer to fill...GOOD!
           if "FillThisBuffer" in logfile_message:
               if allocated_count > 0 and omx_output_buffer_handles[buffer_id] == ALLOCATED:
                  allocated_count-=1
                  omx_output_buffer_handles[buffer_id] = NOT_ALLOCATED
                  print("FillThisBuffer({}) NOT_ALLOCATED; allocated_count: {} ".format(buffer_id,allocated_count))
           # Codec is giving framework filled buffer to render. 
           elif "FillBufferDone" in logfile_message:
               allocated_count+=1
               omx_output_buffer_handles[buffer_id] = ALLOCATED
               print("FillBufferDone({}) ALLOCATED; allocated_count: {} ".format(buffer_id,allocated_count))
           else:
               print("//WARNING: buffer '{}' in below log message, but not FillThisBuffer or FillBufferDone")
               print(logfile_message)

#------------------------------------------------------
# read_log_file
#------------------------------------------------------
def read_log_file():
   with open(logfile_path,'r',encoding='utf-8') as logfile_path_filehandle:
       logfile_message = logfile_path_filehandle.readline()
       while logfile_message:
          #process logfile_message
          process_logfile_message(logfile_message)
          #print(logfile_message)
          logfile_message = logfile_path_filehandle.readline()

#------------------------------------------------------
# print_buffer_dict
#------------------------------------------------------
def print_buffer_dict():
    for buffer_id in omx_output_buffer_handles.keys():
        print("buffer_id:{}: {} ".format(buffer_id,omx_output_buffer_handles[buffer_id]))

#------------------------------------------------------
# MAIN SECTION
#------------------------------------------------------
print_buffer_dict()
read_log_file()
print_buffer_dict()
