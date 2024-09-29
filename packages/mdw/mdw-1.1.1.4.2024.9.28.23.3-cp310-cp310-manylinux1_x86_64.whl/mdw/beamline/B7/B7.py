import os.path


def collect_start(*arg,**args):
    #gui
    CTType = args["CTType"]
    filepath_store_dir = args["filepath_store_dir"]
    # if directory not exist, create it
    #det
    scan_id = args.get("scan_id","none")

    filename1 = "ID21_%s_%s.nxs" % (CTType,str(scan_id))
    filepath1 = filepath_store_dir +"/" + CTType + str(scan_id)+"/"
    if not os.path.exists(filepath1):
        os.makedirs(filepath1)
    filename2 = "ID21_Dhyana_%s_%s_master.h5" % (CTType,str(scan_id))
    filepath2 = filepath_store_dir +"/" + CTType + str(scan_id)+"/"
    if not os.path.exists(filepath2):
        os.makedirs(filepath2)
    filelist_dir_name = [[filepath1,filename1],[filepath2,filename2]]
    args["filelist_dir_name"] = filelist_dir_name
    identify = filepath_store_dir.split("/")[-1] #sample info
    args["identify"] = identify
    return args

    pass
