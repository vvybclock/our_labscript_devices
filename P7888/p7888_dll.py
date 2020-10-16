###########################################################################
#		Written by Enrique Mendez (eqm@mit.edu)	c. 2020	
###########################################################################

from p7888_c_definitions import *
import ctypes


# Test 1: Load the COMCTL.DLL, this is the DLL specified in figure 5.9 of the
# P7888 manual. It appears that its actually "comctl32.dll" as a window search
# revealed.

# Here we load the Dynamic Linked Library that allows sending commands to the
# P7888 card provided we have enabled remote mode in the P7888 server. See
# section 5.2 (p. 5-9) in the p7888 docs.
comtec_dll = ctypes.windll.LoadLibrary("comctl32.dll")

# In section 5.4, they instead reference "dp7888.dll"! This is what is used
# for controlling the server.
dp7888_dll = ctypes.windll.LoadLibrary("dp7888.dll")


HWND = HANDLE

#Specify the functions in CTYPES

#StoreSettingData
#	Stores Settings into the DLL
#		VOID APIENTRY StoreSettingData(ACQSETTING FAR *Setting, int nDisplay);
StoreSettingData = dp7888_dll.StoreSettingData
StoreSettingData.restype = None
StoreSettingData.argtypes = [POINTER(ACQSETTING), c_int]

#GetSettingData
#	Get Settings stored in the DLL
#	Store System Definition into DLL
#		int APIENTRY GetSettingData(ACQSETTING FAR *Setting, int nDisplay);
GetSettingData = dp7888_dll.GetSettingData
GetSettingData.restype = c_int
GetSettingData.argtypes = [POINTER(ACQSETTING), c_int]

#StoreStatusData
#	Store the Status into the DLL
#		VOID APIENTRY StoreStatusData(ACQSTATUS FAR *Status, int nDisplay);
StoreStatusData = dp7888_dll.StoreStatusData 
StoreStatusData.restype = None
StoreStatusData.argtypes = [POINTER(ACQSTATUS), c_int]

#GetStatusData
#	Get the Status
#		int APIENTRY GetStatusData(ACQSTATUS FAR *Status, int nDisplay);
GetStatusData = dp7888_dll.GetStatusData
GetStatusData.restype = c_int
GetStatusData.argtypes = [POINTER(ACQSTATUS), c_int]

#Start
#	Start
#		VOID APIENTRY Start(int nSystem); // Start
Start = dp7888_dll.Start
Start.restype = None
Start.argtypes = [c_int]

#Halt
#	Halt
#		VOID APIENTRY Halt(int nSystem);
Halt = dp7888_dll.Halt
Halt.restype = None
Halt.argtypes = [c_int]

#Continue
#	Continue
#		VOID APIENTRY Continue(int nSystem);
Continue = dp7888_dll.Continue
Continue.restype = None
Continue.argtypes = [c_int]

#NewSetting
#	Indicate new Settings to Server
#		VOID APIENTRY NewSetting(int nDevice);
NewSetting = dp7888_dll.NewSetting
NewSetting.restype = None
NewSetting.argtypes = [c_int]

#ServExec
#	Execute the Server P7888.exe
#		UINT APIENTRY ServExec(HWND ClientWnd);
ServExec = dp7888_dll.ServExec
ServExec.restype = c_uint
ServExec.argtypes = [HWND]

#StoreData
#	 Stores Data pointers into the DLL
#		VOID APIENTRY StoreData(ACQDATA FAR *Data, int nDisplay);
StoreData = dp7888_dll.StoreData
StoreData.restype = None
StoreData.argtypes = [POINTER(ACQDATA), c_int]

#GetData
#	Get Data pointers
#		int APIENTRY GetData(ACQDATA FAR *Data, int nDisplay);
GetData = dp7888_dll.GetData
GetData.restype = c_int
GetData.argtypes = [POINTER(ACQDATA), c_int]

#GetSpec
#	// Get a spectrum value
#		long APIENTRY GetSpec(long i, int nDisplay);
GetSpec = dp7888_dll.GetSpec
GetSpec.restype = c_long
GetSpec.argtypes = [c_long, c_int]

#SaveSetting
#	// Save Settings
#		VOID APIENTRY SaveSetting(void); 
SaveSetting = dp7888_dll.SaveSetting
SaveSetting.restype = None
SaveSetting.argtypes = []

#GetStatus
#	// Request actual Status from Server
#		 int APIENTRY GetStatus(int nDevice);
GetStatus = dp7888_dll.GetStatus
GetStatus.restype = c_int
GetStatus.argtypes = [c_int]

#Erase
#	Erase Spectra
#		VOID APIENTRY Erase(int nSystem); 
Erase = dp7888_dll.Erase
Erase.restype = None
Erase.argtypes = [c_int]

#SaveData
#	Saves data
#		VOID APIENTRY SaveData(int nDevice); 
SaveData = dp7888_dll.SaveData
SaveData.restype = None
SaveData.argtypes = [c_int]

#GetBlock
#	Get a block of spectrum data
#		VOID APIENTRY GetBlock(long FAR *hist, int start, int end, int step, int nDisplay); 
GetBlock = dp7888_dll.GetBlock
GetBlock.restype = None
GetBlock.argtypes = [POINTER(c_long), c_int, c_int, c_int, c_int]

#StoreDefData
#	
#		VOID APIENTRY StoreDefData(ACQDEF FAR *Def);
StoreDefData = dp7888_dll.StoreDefData
StoreDefData.restype = None
StoreDefData.argtypes = [POINTER(ACQDEF)]

#GetDefData
#	Get System Definition
#		int APIENTRY GetDefData(ACQDEF FAR *Def);
GetDefData = dp7888_dll.GetDefData
GetDefData.restype = c_int
GetDefData.argtypes = [POINTER(ACQDEF)]

#LoadData
#	 Loads data
#		VOID APIENTRY LoadData(int nDisplay); 
LoadData = dp7888_dll.LoadData
LoadData.restype = None
LoadData.argtypes = [c_int]

#AddData
#	 Adds data
#		VOID APIENTRY AddData(int nDisplay); 
AddData = dp7888_dll.AddData
AddData.restype = None
AddData.argtypes = [c_int]

#SubData
#	Subtracts data
#		VOID APIENTRY SubData(int nDisplay); 
SubData = dp7888_dll.SubData
SubData.restype = None
SubData.argtypes = [c_int]

#Smooth
#	Smooth data
#		VOID APIENTRY Smooth(int nDisplay); 
Smooth = dp7888_dll.Smooth
Smooth.restype = None
Smooth.argtypes = [c_int]

#NewData
#	Indicate new ROI or string Data
#		VOID APIENTRY NewData(void); 
NewData = dp7888_dll.NewData
NewData.restype = None
NewData.argtypes = []

#HardwareDlg
#	 Calls the Settings dialog box
#		VOID APIENTRY HardwareDlg(int item);
HardwareDlg = dp7888_dll.HardwareDlg
HardwareDlg.restype = None
HardwareDlg.argtypes = [c_int]


#UnregisterClient
#	Clears remote mode from MCDWIN
#		VOID APIENTRY UnregisterClient(void);
UnregisterClient = dp7888_dll.UnregisterClient
UnregisterClient.restype = None
UnregisterClient.argtypes = []

#DestroyClient
#	Close MCDWIN
#		VOID APIENTRY DestroyClient(void); 
DestroyClient = dp7888_dll.DestroyClient
DestroyClient.restype = None
DestroyClient.argtypes = []


#ClientExec
#	Execute the Client MCDWIN.EXE
#		UINT APIENTRY ClientExec(HWND ServerWnd);
ClientExec = dp7888_dll.ClientExec
ClientExec.restype = c_uint
ClientExec.argtypes = [HWND]

#LVGetDat
#	Copies the spectrum to an array
#		int APIENTRY LVGetDat(unsigned long HUGE *datp, int nDisplay);
LVGetDat = dp7888_dll.LVGetDat
LVGetDat.restype = c_int
LVGetDat.argtypes = [POINTER(c_ulong), c_int]

#RunCmd
#	Executes command
#		VOID APIENTRY RunCmd(int nDisplay, LPSTR Cmd);
LPSTR = POINTER(c_char)
RunCmd = dp7888_dll.RunCmd
RunCmd.restype = None
RunCmd.argtypes = [c_int, LPSTR]

#LVGetRoi
#	Copies the ROI boundaries to an array
#		int APIENTRY LVGetRoi(unsigned long FAR *roip, int nDisplay);
LVGetRoi = dp7888_dll.LVGetRoi
LVGetRoi.restype = c_int
LVGetRoi.argtypes = [POINTER(c_ulong), c_int]

#LVGetCnt
#	Copies Cnt numbers to an array
#		int APIENTRY LVGetCnt(double far *cntp, int nDisplay);
LVGetCnt = dp7888_dll.LVGetCnt
LVGetCnt.restype = c_int
LVGetCnt.argtypes = [POINTER(c_double), c_int]

#LVGetStr
#	Copies strings to an array
#		int APIENTRY LVGetStr(char far *strp, int nDisplay);
LVGetStr = dp7888_dll.LVGetStr
LVGetStr.restype = c_int
LVGetStr.argtypes = [POINTER(c_char), c_int]

if __name__ == '__main__':
	settings = ACQSETTING()
	nDisplay = 1

	print(settings.range)
	print(GetSettingData(settings,nDisplay))
	print(settings.range)
