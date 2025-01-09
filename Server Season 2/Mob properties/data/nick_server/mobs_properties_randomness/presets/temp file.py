import MenuNavigation as mnu
import ClickTools as clk
from ClickTools import RightClickAction
from enum import Enum
import traceback



# decorators
def analysis_section(func):
  def wrapper(self, roi: ROI, *args, **kwargs):
    assert roi in self.rois,(f"ROI: {roi} not in {self.rois}\nError occured at:\n{traceback.format_stack()[-2]}")
    mnu.open_camera()
    mnu.open_camera_roi_center()
    mnu.vipercard_roi_analysis(self.offset * roi.index)
    
    result = func(self, roi, *args, **kwargs)
    mnu.close_window()
    return result
  return wrapper
  
  
def edit_roi_section(func):
  def wrapper(self, roi: ROI, *args, **kwargs):
    assert roi in self.rois,(f"ROI {roi} not in {self.rois}\nError occurrec at:\n{traceback.format_stack()[-2]}")
    mnu.open_camera()
    mnu.open_camera_roi_center()
    mnu.vipercard_roi_edit()
    
    result = func(self, roi, *args, **kwargs)
    mnu.close_window()
    return result
  return wrapper
  

########################### ROI status checks ###########################

def list_rois():
  mnu.open_camera()
  mnu.open_camera_roi_center()
  #OCR.Recognize(Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucCameraCenter.tlpButtonControlSplit.panelSettings.ucAllCamerasRois2.panelBase.cardContainerRois.Panel.ViperCard).BlockByText("Sp1").Click()
  container = Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucCameraCenter.tlpButtonControlSplit.panelSettings.ucAllCamerasRois2.panelBase.cardContainerRois.Panel
  for i in range(container.ChildCount):
    card = container.Child(i)
  mnu.close_window()
  
# Passes if all ROIs are deleted
def check_all_rois_deleted():
    mnu.open_camera()
    mnu.open_camera_roi_center()
    if Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucCameraCenter.tlpButtonControlSplit.panelSettings.ucAllCamerasRois2.panelBase.cardContainerRois.Panel.WaitAliasChild("ViperCard", 1000).Exists:
        mnu.close_window()
        tb_info = traceback.format_stack()[-2]
        Log.Error(f"{check_all_rois_deleted.__name__}: ROI not deleted:\tError occured at:\n{tb_info}")
        Runner.Stop(True)
    else:
        pass
    mnu.close_window()

# Returns true if roi is deleted
def check_roi_deleted(name: str) -> bool:
    mnu.open_camera()
    mnu.open_camera_roi_center()
    if Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucCameraCenter.tlpButtonControlSplit.panelSettings.ucAllCamerasRois2.panelBase.cardContainerRois.Panel.WaitAliasChild("ViperCard", 1000).Exists:
      Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucCameraCenter.tlpButtonControlSplit.panelSettings.ucAllCamerasRois2.panelBase.cardContainerRois.Panel.ViperCard.Click(207, 63)
      Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucCameraCenter.tlpButtonControlSplit.panelSettings.ucAllCamerasRois2.panelBase.cardContainerRois.Panel.ViperCard.Click(319, 78)
      labeled_name = Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucRoiCenter.tlpButtonControlSplit.panelSettings.ucRoiNameAndTemp.panelBase.txtName.TextBox.wText
      if labeled_name == name:
        mnu.close_window()
        return False
      else:
        mnu.close_window()
        return True
    else:
      mnu.close_window()
      return True
    mnu.close_window()
    tb_info = traceback.format_stack()[-2]
    Log.Error(f"Error occured at: {tb_info}: Did not check ViperCard existance.")

########################### ROI Manager ###########################

class ROIType(Enum):
  SPOT = "Spot"
  RECTANGLE = "Rectangle"
  LINE = "Line"
  ELLIPSE = "Ellipse"
  ANNULUS = "Annulus"
  POLYGON = "Polygon"
  RULER = "Ruler"
  
class AnalysisType(Enum):
  ABOVE_THRESHOLD = "Above_threshold"
  BELOW_THRESHOLD = "Below_threshold"
  DATA_FEED = "Data_feed"
  DELTA = "Delta"
  PIXELS_PERCENTAGE = "Pixels_percentage"
  RATE_OF_CHANGE = "Rate_of_change"
  STANDARD_DEVIATION = "Standard_deviation"
  GAS_DETECTION = "Gas_detection"

  

'''
Class that holds ROI information
    name: The ROI's name
    type: The ROI's type, look at ROIType above
    x, y: The starting point of the ROI, for Spot it is the point it is on
    
    length, width: Calculates the bottom corner coordinates when dragging the ROI corner
                   Required only for Rectangle, Ellipse, Line, Ruler, and Annulus
    points:        A list of points as tuples [(x1,y1), (x2,y2)]. Required for Polygon only
'''
class ROI:
    def __init__(self, name: str, type: ROIType, x=800, y=400, width: int=None, height: int=None, points: list=None):
      self.type = type
      self.index = None
      self.analysis = []
      self.shape_detection = []
      self.name = name
      self.outer_name = None
      if type == ROIType.ANNULUS:
        self.outer_name = f"{name}_Outer"
      if type == ROIType.POLYGON:
        if len(points) < 3:
          tb_info = traceback.format_stack()[-2]
          Log.Error(f"Invalid number of points: Class: {self.__class__.__name__}\tError occured at: {tb_info}")
          Runner.Stop(True)
        self.points = points
      else:
        self.x = x
        self.y = y
      if type != ROIType.SPOT and type != ROIType.POLYGON:
        self.height = height
        self.width = width
        
      # name & temperature
      self.local_params = False
      self.emissivity = 1.00
      self.reflected_temperature = 0.00
      self.distance = 0.00
      self.boundary_temp = False
      
      # ROI display
      self.min_temp_roi = True
      self.max_temp_roi = True
      self.avg_temp_roi = True
      self.hot_spot = False
      self.cold_spot = False
      self.hide_roi = False
      self.hide_name = False
      self.min_temp_pane = True
      self.max_temp_pane = True
      self.avg_temp_pane = True
      
      # TODO: ROI colors
      
        
    def __str__(self):
      return f"ROI: {self.name}, type: {self.type}, index: {self.index}"
        


# Use the ROIManager to manipulate ROI objects.  
class ROIManager:
  
  offset = 110
  
  valid_audio_types = ["No_audio", "Audio_bamboo", "Audio_bell", "Audio_buzz", "Audio_chirp", "Audio_cricket", "Audio_ebt", "Audio_magic", "Audio_siren", "Audio_swoosh", "Audio_wakeup"]
  valid_output_types = ["Alarm", "Feed"]
  valid_temp_types = ["Minimum_temperature", "Maximum_temperature", "Average_temperature"]
  valid_threshold_types = ["Over_threshold_alarm", "Over_threshold_feed", "Under_threshold_alarm", "Under_threshold_feed"]
  valid_period_types = ["Miliseconds", "Seconds", "Minutes", "Hours", "Days"]
    
  def __init__(self):
    self.rois = []
    
  def update_indices(self):
    for i, roi in enumerate(self.rois):
      roi.index = i
  
  def get_roi_by_name(self, name) -> ROI:
    for roi in self.rois:
      if roi.name == name:
        return ROI
    tb_info = traceback.format_stack()[-2]
    Log.Error(f"ROI not found with {name}\tError occured at:\n{tb_info}")
    Runner.Stop(True)
    
  def get_roi_by_index(self, index: int) -> ROI:
    for roi in self.rois:
      if roi.index == index:
        return ROI
    tb_info = traceback.format_stack()[-2]
    Log.Error(f"ROI not found with index: {index}\tError occured at: {tb_info}")
    Runner.Stop(True)
  
  def get_outer_roi(annulus_roi: ROI):
    for roi in self.rois:
      if roi.name == annulus_roi.outer_name:
        return roi
    return None
    
  def list_rois(self):
    for roi in self.rois:
      Log.Message(f"ROI Name: {roi.name}, Index: {roi.index}")

  def create_roi(self, roi: ROI):
    if roi.index is None:
      if roi.type == ROIType.ANNULUS:
        self.rois.append(roi)
        self.rois.append(ROI(roi.outer_name, roi.type))
      else:
        self.rois.append(roi)
      self.update_indices()
      if (roi.type == ROIType.POLYGON) and (roi.points is not None):
        drag_create_roi(roi)
        mnu.open_camera()
        mnu.open_camera_roi_center()
        mnu.vipercard_roi_edit(self.offset * (roi.index))
        Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucRoiCenter.tlpButtonControlSplit.panelSettings.ucRoiNameAndTemp.panelBase.txtName.TextBox.SetText(roi.name)
        Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucRoiCenter.tlpButtonControlSplit.panelSettings.ucRoiNameAndTemp.panelButtons.panelOkay.buttonOkay.Click()
        mnu.close_window()
      elif (roi.type == ROIType.SPOT):
        drag_create_roi(roi)
        mnu.open_camera()
        mnu.open_camera_roi_center()
        mnu.vipercard_roi_edit(self.offset * (roi.index))
        Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucRoiCenter.tlpButtonControlSplit.panelSettings.ucRoiNameAndTemp.panelBase.txtName.TextBox.SetText(roi.name)
        Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucRoiCenter.tlpButtonControlSplit.panelSettings.ucRoiNameAndTemp.panelButtons.panelOkay.buttonOkay.Click()
        mnu.close_window()
      elif (roi.width is not None) and (roi.height is not None):
        drag_create_roi(roi)
        mnu.open_camera()
        mnu.open_camera_roi_center()
        mnu.vipercard_roi_edit(self.offset * (roi.index))
        Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucRoiCenter.tlpButtonControlSplit.panelSettings.ucRoiNameAndTemp.panelBase.txtName.TextBox.SetText(roi.name)
        Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucRoiCenter.tlpButtonControlSplit.panelSettings.ucRoiNameAndTemp.panelButtons.panelOkay.buttonOkay.Click()
        mnu.close_window()
      else:
        clk.right_click_action(RightClickAction.ROIS, roi.x, roi.y)
        OCR.Recognize(Aliases.ViperVision.RadDropDownMenu).BlockByText("New ROI").Click()
        OCR.Recognize(Aliases.ViperVision.RadDropDownMenu2).BlockByText(roi.type.value).Click()
        mnu.open_camera()
        mnu.open_camera_roi_center()
        mnu.vipercard_roi_edit(self.offset * (roi.index))
        Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucRoiCenter.tlpButtonControlSplit.panelSettings.ucRoiNameAndTemp.panelBase.txtName.TextBox.SetText(roi.name)
        Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucRoiCenter.tlpButtonControlSplit.panelSettings.ucRoiNameAndTemp.panelButtons.panelOkay.buttonOkay.Click()
        mnu.close_window()
      if roi.type == ROIType.ANNULUS:
        mnu.vipercard_roi_edit(self.offset * (roi.index + 1))
        Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucRoiCenter.tlpButtonControlSplit.panelSettings.ucRoiNameAndTemp.panelBase.txtName.TextBox.SetText(roi.outer_name)
        Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucRoiCenter.tlpButtonControlSplit.panelSettings.ucRoiNameAndTemp.panelButtons.panelOkay.buttonOkay.Click()
        mnu.close_window()
    else:
      tb_info = traceback.format_stack()[-2]
      Log.Error(f"{self.create_roi.__name__}: ROI name: {roi.name}, already taken:\tError occured at: {tb_info}")
      Runner.Stop(True)
    
    
  def click_delete_roi(self, roi: ROI):
      if roi in self.rois:
        if roi.type == ROIType.ANNULUS:
          outer_roi = self.get_outer_roi(roi)
          if outer_roi:
            clk.right_click_action(RightClickAction.ROIS, outer_roi.x, outer_roi.y)
            OCR.Recognize(Aliases.ViperVision.RadDropDownMenu).BlockByText(outer_roi.name).Click()
            OCR.Recognize(Aliases.ViperVision.RadDropDownMenu2).BlockByText("Delete").Click()
            self.rois.remove(outer_roi)
        else:
          clk.right_click_action(RightClickAction.ROIS, roi.x, roi.y)
          OCR.Recognize(Aliases.ViperVision.RadDropDownMenu).BlockByText(roi.name).Click()
          OCR.Recognize(Aliases.ViperVision.RadDropDownMenu2).BlockByText("Delete").Click()
          self.rois.remove(roi)
        self.update_indices()
      else:
        tb_info = traceback.format_stack()[-2]
        Log.Error(f"ROI not found in ', '.join({self.rois})\tError occured at: {tb_info}")
        Runner.Stop(True)
  
  # Would much rather use this to delete ROIs than click_delete_roi
  def delete_roi(self, roi: ROI):
    if roi in self.rois:
      mnu.open_camera()
      mnu.open_camera_roi_center()
      mnu.vipercard_roi_edit(self.offset * roi.index)
      mnu.close_window()
      mnu.vipercard_roi_remove(self.offset * roi.index)
      mnu.close_window()
      
      self.rois.remove(roi)
      self.update_indices()
    else:
      tb_info = traceback.format_stack()[-2]
      Log.Error(f"ROI not found in ', '.join({self.rois})\tError occured at: {tb_info}")
      Runner.Stop(True)
      
          ################ Analysis section #################
  @analysis_section
  def above_threshold(self, roi: ROI, temp_type="Minimum_temperature", temp_threshold=30.00, deferment_period=0, audio="No_audio"):
      Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucAnalysisCenter.tlpButtonControlSplit.tlpSettingsButtons.labelAbove.Click()
      Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucAnalysisCenter.tlpButtonControlSplit.panelSettings.ucAnalysisAbove.panelBase.dropdownType.temperatureLabel.Click()
      if temp_type not in self.valid_temp_types:
        tb_info = traceback.format_stack()[-2]
        Log.Error(f"{self.above_threshold.__name__}: Invalid temp_type. Expected {', '.join(self.valid_temp_types)}\tError occured at: {tb_info}")
        Runner.Stop(True)
      temp_alias = f"Aliases.ViperVision.ToolStripDropDown.TableLayoutPanel.{temp_type}"
      eval(temp_alias).Click()
      Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucAnalysisCenter.tlpButtonControlSplit.panelSettings.ucAnalysisAbove.panelBase.numThreshold.RadSpinEditor.wValue = temp_threshold
      Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucAnalysisCenter.tlpButtonControlSplit.panelSettings.ucAnalysisAbove.panelBase.numDeferment.RadSpinEditor.wValue = deferment_period
      Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucAnalysisCenter.tlpButtonControlSplit.panelSettings.ucAnalysisAbove.panelBase.dropdownAlarmAudio.Label.Click()
      if audio not in self.valid_audio_types:
        tb_info = traceback.format_stack()[-2]
        Log.Error(f"{self.above_threshold.__name__}: Invalid audio. Expected {', '.join(self.valid_audio_types)}\tError occured at: {tb_info}")
        Runner.Stop(True)
      audio_alias = f"Aliases.ViperVision.ToolStripDropDown.TableLayoutPanel.{audio}"
      eval(audio_alias).Click()
      Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucAnalysisCenter.tlpButtonControlSplit.panelSettings.ucAnalysisAbove.panelButtons.panelOkay.buttonOkay.Click()
      roi.analysis.append(AnalysisType.ABOVE_THRESHOLD)
      
        
  @analysis_section    
  def below_threshold(self, roi: ROI, temp_type="Minimum_temperature", temp_threshold=30.00, deferment_period=0, audio="No_audio"):
        Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucAnalysisCenter.tlpButtonControlSplit.tlpSettingsButtons.labelBelow.Click()
        Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucAnalysisCenter.tlpButtonControlSplit.panelSettings.ucAnalysisBelow.panelBase.dropdownType.temperatureLabel.Click()
        assert temp_type in self.valid_temp_types,(f"Expected {', '.join(self.valid_temp_types)} but got '{temp_type}'\nError occured at:\n{traceback.format_stack()[-2]}")

        temp_alias = f"Aliases.ViperVision.ToolStripDropDown.TableLayoutPanel.{temp_type}"
        eval(temp_alias).Click()
        Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucAnalysisCenter.tlpButtonControlSplit.panelSettings.ucAnalysisBelow.panelBase.numThreshold.RadSpinEditor.wValue = temp_threshold
        Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucAnalysisCenter.tlpButtonControlSplit.panelSettings.ucAnalysisBelow.panelBase.numDeferment.RadSpinEditor.wValue = deferment_period
        Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucAnalysisCenter.tlpButtonControlSplit.panelSettings.ucAnalysisBelow.panelBase.dropdownAlarmAudio.Label.Click()
        assert audio in self.valid_audio_types,(f"Expected {', '.join(self.valid_audio_types)} but got '{audio}'\nError occured at:\n{traceback.format_stack()[-2]}")

        audio_alias = f"Aliases.ViperVision.ToolStripDropDown.TableLayoutPanel.{audio}"
        eval(audio_alias).Click()
        Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucAnalysisCenter.tlpButtonControlSplit.panelSettings.ucAnalysisBelow.panelButtons.panelOkay.buttonOkay.Click()
        roi.analysis.append(AnalysisType.BELOW_THRESHOLD)

  
  @analysis_section      
  def data_feed(self, roi: ROI, temp_type="Minimum_temperature"):
        valid_data_feed_temp_types = ["Minimum_temperature", "Maximum_temperature", "Average_temperature", "ROI_width", "ROI_center_X_position", "ROI_center_Y_position", "ROI_height", "ROI_X_position", "ROI_Y_position"]
                
        assert temp_type in self.valid_temp_types,(f"Expected {', '.join(self.valid_temp_types)} but got '{temp_type}'\nError occured at:\n{traceback.format_stack()[-2]}") 
        assert temp_type in valid_data_feed_temp_types,(f"Expected {', '.join(valid_data_feed_temp_types)} but got '{temp_type}'\nError occured at:\n{traceback.format_stack()[-2]}")
        Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucAnalysisCenter.tlpButtonControlSplit.tlpSettingsButtons.labelFeed.Click()
        Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucAnalysisCenter.tlpButtonControlSplit.panelSettings.ucAnalysisFeed.panelBase.dropdownType.temperatureLabel.Click()

        
        temp_alias = f"Aliases.ViperVision.ToolStripDropDown.TableLayoutPanel.{temp_type}"
        eval(temp_alias).click()
        Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucAnalysisCenter.tlpButtonControlSplit.panelSettings.ucAnalysisFeed.panelButtons.panelOkay.buttonOkay.Click()
        roi.analysis.append(AnalysisType.DATA_FEED)

        
  @analysis_section      
  def delta(self, roi: ROI, second_roi: ROI, measurement_1="AverageValue", measurement_2="AverageValue", output_type="Alarm", temp_threshold=30.00, deferment_period=0, audio_type="No_audio"):
            Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucAnalysisCenter.tlpButtonControlSplit.tlpSettingsButtons.labelDelta.Click()
            if (second_roi is not None) and (second_roi in self.rois):
                assert output_type in self.valid_output_types,(f"Expected {', '.join(self.valid_output_types)} but got '{output_type}'\nError occured at:\n{traceback.format_stack()[-2]}")
                assert audio_type in self.valid_audio_types,(f"Expected {', '.join(self.valid_audio_types)} but got '{audio_type}'\nError occured at:\n{traceback.format_stack()[-2]}")
                if roi.type.value == "Spot":
                  Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucAnalysisCenter.tlpButtonControlSplit.panelSettings.ucAnalysisDelta.panelBase.dropdownM1.measurementLabel1.Click()
                  if measurement_1 != "AverageValue":
                    tb_info = traceback.format_stack()[-2]
                    Log.Error("{self.delta.__name__}: Spot Measurement 1 value must be 'AverageValue'\tError occured at: {tb_info}")
                    Runner.Stop(True)
                  
                  OCR.Recognize(Aliases.ViperVision.ToolStripDropDown.TableLayoutPanel).BlockByText(f"{self.name.value} - AverageValue").Click()
                  Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucAnalysisCenter.tlpButtonControlSplit.panelSettings.ucAnalysisDelta.panelBase.dropdownM2.Label.Click()
                  if (second_roi.type == ROIType.SPOT) and (measurement_2 != "AverageValue"):
                      tb_info = traceback.format_stack()[-2]
                      Log.Error(f"{self.delta_add.__name__}: Second SPOT roi must measure 'AverageValue'\tError occured at: {tb_info}")
                      Runner.Stop(True)
                  elif second_roi.type == ROIType.ANNULUS:
                      tb_info = traceback.format_stack()[-2]
                      Log.Error(f"{self.delta.__name__}: Second ROI cannot be 'Annulus'\tError occured at: {tb_info}")
                      Runner.Stop(True)
                  elif second_roi.type == ROIType.SPOT:
                      OCR.Recognize(Aliases.ViperVision.ToolStripDropDown.TableLayoutPanel).BlockByText(f"{second_roi.name} - AverageValue")
                  else:
                      OCR.Recognize(Aliases.ViperVision.ToolStripDropDown.TableLayoutPanel).BlockByText(f"{second_roi.name} - {measurement_2}").Click()
                  
                  Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucAnalysisCenter.tlpButtonControlSplit.panelSettings.ucAnalysisDelta.panelBase.dropdownOutput.Label.Click() 
                  output_alias = f"Aliases.ViperVision.ToolStripDropDown.TableLayoutPanel.{output_type}"
                  eval(output_alias).Click()
                  Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucAnalysisCenter.tlpButtonControlSplit.panelSettings.ucAnalysisDelta.panelBase.numThreshold.RadSpinEditor.wValue = temp_threshold
                  Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucAnalysisCenter.tlpButtonControlSplit.panelSettings.ucAnalysisDelta.panelBase.numDeferment.RadSpinEditor.wValue = deferment_period
                  Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucAnalysisCenter.tlpButtonControlSplit.panelSettings.ucAnalysisDelta.panelBase.VScroll.Pos = 114
                  Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucAnalysisCenter.tlpButtonControlSplit.panelSettings.ucAnalysisDelta.panelBase.dropdownAlarmAudio.Label.click()
                  audio_alias = f"Aliases.ViperVision.ToolStripDropDown.TableLayoutPanel.{audio_type}"
                  eval(audio_alias).Click()
                  roi.analysis.append(AnalysisType.DATA_FEED)
                  Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucAnalysisCenter.tlpButtonControlSplit.panelSettings.ucAnalysisDelta.panelButtons.panelOkay.buttonOkay.Click()
                  
                else:
                  Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucAnalysisCenter.tlpButtonControlSplit.panelSettings.ucAnalysisDelta.panelBase.dropdownM1.measurementLabel1.Click()
                  OCR.Recognize(Aliases.ViperVision.ToolStripDropDown.TableLayoutPanel).BlockByText(f"{roi.name} - {measurement_1}").Click()
                  Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucAnalysisCenter.tlpButtonControlSplit.panelSettings.ucAnalysisDelta.panelBase.dropdownM2.Label.Click()
                  
                  if (second_roi.type == ROIType.SPOT) and (measurement_2 != "AverageValue"):
                      tb_info = traceback.format_stack()[-2]
                      Log.Error(f"{self.delta.__name__}: Second SPOT roi must measure 'AverageValue'\tError occured at: {tb_info}")
                      Runner.Stop(True)
                  elif second_roi.type == ROIType.ANNULUS:
                      tb_info = traceback.format_stack()[-2]
                      Log.Error(f"{self.delta.__name__}: Second ROI cannot be 'Annulus'\tError occured at: {tb_info}")
                      Runner.Stop(True)
                  elif second_roi.type == ROIType.SPOT:
                      OCR.Recognize(Aliases.ViperVision.ToolStripDropDown.TableLayoutPanel).BlockByText(f"{second_roi.name} - AverageValue")
                  else:
                      OCR.Recognize(Aliases.ViperVision.ToolStripDropDown.TableLayoutPanel).BlockByText(f"{second_roi.name} - {measurement_2}").Click()
                  
                  Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucAnalysisCenter.tlpButtonControlSplit.panelSettings.ucAnalysisDelta.panelBase.dropdownOutput.Label.Click()
                  output_alias = f"Aliases.ViperVision.ToolStripDropDown.TableLayoutPanel.{output_type}"
                  eval(output_alias).Click()
                  Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucAnalysisCenter.tlpButtonControlSplit.panelSettings.ucAnalysisDelta.panelBase.numThreshold.RadSpinEditor.wValue = temp_threshold
                  Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucAnalysisCenter.tlpButtonControlSplit.panelSettings.ucAnalysisDelta.panelBase.numDeferment.RadSpinEditor.wValue = deferment_period
                  Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucAnalysisCenter.tlpButtonControlSplit.panelSettings.ucAnalysisDelta.panelBase.VScroll.Pos = 114
                  Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucAnalysisCenter.tlpButtonControlSplit.panelSettings.ucAnalysisDelta.panelBase.dropdownAlarmAudio.Label.click()
                  audio_alias = f"Aliases.ViperVision.ToolStripDropDown.TableLayoutPanel.{audio_type}"
                  eval(audio_alias).Click()
                  roi.analysis.append(AnalysisType.DATA_FEED)
                  Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucAnalysisCenter.tlpButtonControlSplit.panelSettings.ucAnalysisDelta.panelButtons.panelOkay.buttonOkay.Click()
                  
            elif roi.type.value == "Annulus":
                Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucAnalysisCenter.tlpButtonControlSplit.panelSettings.ucAnalysisDelta.panelBase.dropdownOutput.Label.Click()
                output_alias = f"Aliases.ViperVision.ToolStripDropDown.TableLayoutPanel.{output_type}"
                eval(output_alias).Click()
                Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucAnalysisCenter.tlpButtonControlSplit.panelSettings.ucAnalysisDelta.panelBase.numThreshold.RadSpinEditor.wValue = temp_threshold
                Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucAnalysisCenter.tlpButtonControlSplit.panelSettings.ucAnalysisDelta.panelBase.numDeferment.RadSpinEditor.wValue = deferment_period
                Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucAnalysisCenter.tlpButtonControlSplit.panelSettings.ucAnalysisDelta.panelBase.VScroll.Pos = 114
                Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucAnalysisCenter.tlpButtonControlSplit.panelSettings.ucAnalysisDelta.panelBase.dropdownAlarmAudio.Label.click()
                audio_alias = f"Aliases.ViperVision.ToolStripDropDown.TableLayoutPanel.{audio_type}"
                eval(audio_alias).Click()
                roi.analysis.append(AnalysisType.DATA_FEED)
                Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucAnalysisCenter.tlpButtonControlSplit.panelSettings.ucAnalysisDelta.panelButtons.panelOkay.buttonOkay.Click()
            
            else:
                tb_info = traceback.format_stack()[-2]
                Log.Error(f"{self.delta.__name__}: Secondary ROI does not exist\tError occured at: {tb_info}")
                Runner.Stop(True)

                
                
  @analysis_section              
  def pixels_percentage(self, roi: ROI, temp_threshold=30.00, pixel_percent=50, output_type="Over_threshold_alarm", deferment_period=0, audio_type="No_audio"):
      assert audio_type in self.valid_audio_types,(f"Expected {', '.join(self.valid_audio_types)} but got '{audio_type}'\nError occured at:\n{traceback.format_stack()[-2]}")
      assert output_type in self.valid_threshold_types,(f"Expected {', '.join(self.valid_threshold_types)} but got '{output_type}'\nError occured at:\n{traceback.format_stack()[-2]}")
      
      Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucAnalysisCenter.tlpButtonControlSplit.tlpSettingsButtons.labelPixelsOver.Click()
      Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucAnalysisCenter.tlpButtonControlSplit.panelSettings.ucAnalysisPixelsOverUnder.panelBase.numThreshold.RadSpinEditor.wValue = temp_threshold
      Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucAnalysisCenter.tlpButtonControlSplit.panelSettings.ucAnalysisPixelsOverUnder.panelBase.numPercentage.RadSpinEditor.wValue = pixel_percent
      Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucAnalysisCenter.tlpButtonControlSplit.panelSettings.ucAnalysisPixelsOverUnder.panelBase.dropdownOutput.Label.Click()
      output_alias = f"Aliases.ViperVision.ToolStripDropDown.TableLayoutPanel.{output_type}"      
      eval(output_alias).Click()
      Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucAnalysisCenter.tlpButtonControlSplit.panelSettings.ucAnalysisPixelsOverUnder.panelBase.numDeferment.RadSpinEditor.wValue = deferment_period
      Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucAnalysisCenter.tlpButtonControlSplit.panelSettings.ucAnalysisPixelsOverUnder.panelBase.VScroll.Pos = 23
      Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucAnalysisCenter.tlpButtonControlSplit.panelSettings.ucAnalysisPixelsOverUnder.panelBase.dropdownAlarmAudio.Label.Click()
      audio_alias = f"Aliases.ViperVision.ToolStripDropDown.TableLayoutPanel.{audio_type}"
      eval(audio_alias).Click()
      Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucAnalysisCenter.tlpButtonControlSplit.panelSettings.ucAnalysisPixelsOverUnder.panelButtons.panelOkay.buttonOkay.Click()
      roi.analysis.append(AnalysisType.PIXELS_PERCENTAGE)

   
  @analysis_section     
  def rate_of_change(self, roi: ROI, temp_type="Minimum_temperature", interval=30, time_period="Seconds", calc_at_end=False, alarm_type="None", temp_threshold=30.00, audio_type="No_audio"):
        Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucAnalysisCenter.tlpButtonControlSplit.tlpSettingsButtons.labelRoc.Click()
        Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucAnalysisCenter.tlpButtonControlSplit.panelSettings.ucAnalysisRoc.panelBase.dropdownType.Label.Click()
        assert temp_type in self.valid_temp_types,(f"Expected {', '.join(self.valid_temp_types)} but got '{temp_type}'\nError occured at:\n{traceback.format_stack()[-2]}")
        assert time_period in self.valid_period_types,(f"Expected {', '.join(self.valid_period_types)} but got '{time_period}'\nError occured at:\{traceback.format_stack()[-2]}")
        assert alarm_type in ["None", "Above", "Below"],(f"Expected 'None', 'Above', 'Below' but got '{alarm_type}'\nError occured at:\n{traceback.format_stack()[-2]}")
        assert audio_type in self.valid_audio_types,(f"Expected {', '.join(self.valid_audio_types)} bu got {audio_type}\nError occured at:\n{traceback.format_stack()[-2]}")

        temp_alias = f"Aliases.ViperVision.ToolStripDropDown.TableLayoutPanel.{temp_type}"
        eval(temp_alias).Click()
        Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucAnalysisCenter.tlpButtonControlSplit.panelSettings.ucAnalysisRoc.panelBase.numInterval.RadSpinEditor.wValue = interval
              
        Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucAnalysisCenter.tlpButtonControlSplit.panelSettings.ucAnalysisRoc.panelBase.dropdownInterval.Label.Click()
        period_alias = f"Aliases.ViperVision.ToolStripDropDown.TableLayoutPanel.{time_period}"
        eval(period_alias).Click()
                
        if calc_at_end:
          Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucAnalysisCenter.tlpButtonControlSplit.panelSettings.ucAnalysisRoc.chkCalcOnlyOnInterval.Click()
              
        Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucAnalysisCenter.tlpButtonControlSplit.panelSettings.ucAnalysisRoc.panelBase.dropdownAlarmType.Label.Click()

        alarm_alias = f"Aliases.ViperVision.ToolStripDropDown.TableLayoutPanel.{alarm_type}"
        getattr(Aliases.ViperVision.ToolStripDropDown.TableLayoutPanel, alarm_type).CLick()
                
        Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucAnalysisCenter.tlpButtonControlSplit.panelSettings.ucAnalysisRoc.panelBase.VScroll.Pos = 174
        Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucAnalysisCenter.tlpButtonControlSplit.panelSettings.ucAnalysisRoc.panelBase.numThreshold.RadSpinEditor.wValue = temp_threshold
        Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucAnalysisCenter.tlpButtonControlSplit.panelSettings.ucAnalysisRoc.panelBase.dropdownAlarmAudio.Label.Click()  
        audio_alias = f"Aliases.ViperVision.ToolStripDropDown.TableLayoutPanel.{audio_type}"
        eval(audio_alias).Click()
        Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucAnalysisCenter.tlpButtonControlSplit.panelSettings.ucAnalysisRoc.panelButtons.panelOkay.buttonOkay.Click()
        roi.analysis.append(AnalysisType.RATE_OF_CHANGE)
        
           
  @analysis_section           
  def standard_deviation(self, roi: ROI, temp_type="Minimum_temperature"):
      assert temp_type in self.valid_temp_types,(f"Expected {', '.join(self.valid_temp_types)} but got '{temp_type}'\nError occured at:\n{traceback.format_stack()[-2]}")
      
      Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucAnalysisCenter.tlpButtonControlSplit.tlpSettingsButtons.labelStandardDeviation.Click()
      Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucAnalysisCenter.tlpButtonControlSplit.panelSettings.ucAnalysisStandardDeviation.panelBase.dropdownType.Label.Click()
      temp_alias = f"Aliases.ViperVision.ToolStripDropDown.TableLayoutPanel.{temp_type}"
      eval(temp_alias).Click()
      roi.analysis.append(AnalysisType.STANDARD_DEVIATION)
      Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucAnalysisCenter.tlpButtonControlSplit.panelSettings.ucAnalysisStandardDeviation.panelButtons.panelOkay.buttonOkay.Click()

        
  @analysis_section      
  def gas_detection(self, roi: ROI, deferment_period=0, audio_type="No_audio"):
      assert audio_type in self.valid_audio_types,(f"Expected {', '.join(self.valid_audio_types)} but got '{audio_type}'\nError occured at:\n{traceback.format_stack()[-2]}")
      
      Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucAnalysisCenter.tlpButtonControlSplit.tlpSettingsButtons.labelGasDetection.Click()
      Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucAnalysisCenter.tlpButtonControlSplit.panelSettings.ucAnalysisGasDetection.panelBase.numDeferment.RadSpinEditor.wValue = deferment_period
      Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucAnalysisCenter.tlpButtonControlSplit.panelSettings.ucAnalysisGasDetection.panelBase.dropdownAlarmAudio.Label.Click()
      audio_alias = f"Aliases.ViperVision.ToolStripDropDown.TableLayoutPanel.{audio_type}"
      eval(audio_alias).Click()
      roi.analysis.append(AnalysisType.GAS_DETECTION)
      Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucAnalysisCenter.tlpButtonControlSplit.panelSettings.ucAnalysisGasDetection.panelButtons.panelOkay.buttonOkay.Click()

                      
  def delete_analysis(self, roi: ROI, analysis: AnalysisType):
    if roi in self.rois:
      if analysis in roi.analysis:
        mnu.open_camera()
        mnu.open_camera_roi_center()
        mnu.vipercard_roi_edit(self.offset * roi.index)
        mnu.roi_edit_analysis_center()
        analysis_index = roi.analysis.index(analysis)
        Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucRoiCenter.tlpButtonControlSplit.panelSettings.ucRoiAnalyses.panelBase.cardContainerAnalyses.Panel.Click(340,30 + (self.offset * analysis_index))
        Aliases.ViperVision.dlgViperImagingNotificationDeletingAnalysis.btnYes.ClickButton()
      else:
        tb_info = traceback.format_stack()[-2]
        Log.Error(f'{self.delete_analysis.__name__}: {analysis} not found in {roi.analysis}\tError occured at: {tb_info}')
    else:
      tb_info = traceback.format_stack()[-2]
      Log.Error(f'{self.delete_analysis.__name__}: {roi} not found in {self.rois}\tError occured at: {tb_info}')
      Runner.Stop(True)
      
      
  @analysis_section
  def delete_all_analysis(self, roi: ROI):
      mnu.roi_edit_analysis_center()
      while Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucRoiCenter.tlpButtonControlSplit.panelSettings.ucRoiAnalyses.panelBase.cardContainerAnalyses.Panel.ViperCard.Exists:
        mnu.analysis_center_remove()
        Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucRoiCenter.tlpButtonControlSplit.panelSettings.ucRoiAnalyses.panelButtons.panelOkay.buttonOkay.Click()

        
      
  ##################### Edit ROI Section ########################
  
  @edit_roi_section
  def edit_name_and_temperature(self, roi:ROI, name: str=None, local_params: bool=None, emissivity: float=None, reflected_temp: float=None, distance: float=None, boundary_temp: bool=None):
        mnu.roi_edit_name_and_temp()
        if name is not None:
          Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucRoiCenter.tlpButtonControlSplit.panelSettings.ucRoiNameAndTemp.panelBase.txtName.TextBox.Keys(name)
          roi.name = name
        if local_params is not None:
          if (roi.local_params == False) and (local_params == True):
            Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucRoiCenter.tlpButtonControlSplit.panelSettings.ucRoiNameAndTemp.panelBase.chkLocalParameters.Click(40, 16)
            roi.local_params = True
          elif (roi.local_params == True) and (local_params == False):
            Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucRoiCenter.tlpButtonControlSplit.panelSettings.ucRoiNameAndTemp.panelBase.chkLocalParameters.Click(40, 16)
            roi.local_params = False
          else:
            Log.Warning(f"{str(roi)} local_params is already set to: {local_params}")
        if emissivity is not None:
          assert 1>= emissivity >=0
          Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucRoiCenter.tlpButtonControlSplit.panelSettings.ucRoiNameAndTemp.panelBase.numEmissivity.RadSpinEditor.HostedTextBoxBase.Keys(str(emissivity))
          roi.emissivity = emissivity
        if reflected_temp is not None:
          Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucRoiCenter.tlpButtonControlSplit.panelSettings.ucRoiNameAndTemp.panelBase.numReflectedTemp.RadSpinEditor.HostedTextBoxBase.Keys(str(reflected_temp))
          roi.reflected_temp = reflected_temp
        if distance is not None:
          Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucRoiCenter.tlpButtonControlSplit.panelSettings.ucRoiNameAndTemp.panelBase.numDistance.RadSpinEditor.HostedTextBoxBase.Keys(str(distance))
          roi.distance = distance
        if boundary_temp is not None:
          if (roi.boundary_temp == False) and (boundary_temp == True):
              Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucRoiCenter.tlpButtonControlSplit.panelSettings.ucRoiNameAndTemp.panelBase.chkBoundaryTemp.Click(40, 18)
              roi.boundary_temp = True
          elif (roi.boundary_temp == True) and (boundary_temp == False):
              Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucRoiCenter.tlpButtonControlSplit.panelSettings.ucRoiNameAndTemp.panelBase.chkBoundaryTemp.Click(40, 18)
              roi.boundary_temp = False
          else:
              Log.Warning(f"{str(roi)} boundary_temp is already set to: {boundary_temp}")
        Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucRoiCenter.tlpButtonControlSplit.panelSettings.ucRoiNameAndTemp.panelButtons.panelOkay.buttonOkay.Click()

  @edit_roi_section   
  def edit_roi_display(self, roi: ROI, 
    min_temp_roi: bool=None, 
    max_temp_roi: bool=None, 
    avg_temp_roi: str=None, 
    hot_spot: bool=None, 
    cold_spot: bool=None, 
    hide_roi:bool=None,
    hide_name:bool=None,
    min_temp_pane: bool=None,
    max_temp_pane: bool=None,
    avg_temp_pane: bool=None
    ):
      mnu.roi_edit_roi_display()
      def button_check(roi_value, parameter, chk_name: str):
        if (roi_value == False) and (parameter == True):
          button_alias = f"Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucRoiCenter.tlpButtonControlSplit.panelSettings.ucRoiDisplay.panelBase.{chk_name}"
          eval(button_alias).Click(40, 16)
          roi_value = True
        elif (roi_value == True) and (parameter == False):
          button_alias = f"Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucRoiCenter.tlpButtonControlSplit.panelSettings.ucRoiDisplay.panelBase.{chk_name}"
          eval(button_alias).Click(40, 16)
          roi_value = False
        else:
          Log.Warning(f"{str(roi)} {roi_value} is already set to: {parameter}")
        
      button_mapping = {
        'chkDisplayMinTemp': (roi.min_temp_roi, min_temp_roi),
        'chkDisplayMaxTemp': (roi.max_temp_roi, max_temp_roi),
        'chkDisplayAvgTemp': (roi.avg_temp_roi, avg_temp_roi),
        'chkDisplayHotSpot': (roi.hot_spot, hot_spot),
        'chkDisplayColdSpot': (roi.cold_spot, cold_spot),
        'chkHideRoi': (roi.hide_roi, hide_roi),
        'chkHideLabel': (roi.hide_name, hide_name),
        'chkMinTempSummary': (roi.min_temp_pane, min_temp_pane),
        'chkMaxTempSummary': (roi.max_temp_pane, max_temp_pane),
        'chkAvgTempSummary': (roi.avg_temp_pane, avg_temp_pane)
      }
        
      for chk_name, (roi_value, parameter) in button_mapping.items():
        if chk_name == 'chkDisplayColdSpot':
          Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucRoiCenter.tlpButtonControlSplit.panelSettings.ucRoiDisplay.panelBase.VScroll.Pos = 395
        if parameter is not None:
          button_check(roi_value, parameter, chk_name)
      Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucRoiCenter.tlpButtonControlSplit.panelSettings.ucRoiDisplay.panelButtons.panelOkay.buttonOkay.Click()
    
    
  # Shape Detection
  
  @edit_roi_section
  def add_shape_detection(self, roi: ROI, name: str, 
    detection_name: str='Circles', 
    location_accuracy: int=75,
    size_accuracy: int=75,
    canny_threshold: int=100,
    threshold_linking: int=100,
    detection_frames: int=5
    ):
      mnu.roi_edit_shape_detection()
      Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucRoiCenter.tlpButtonControlSplit.panelSettings.ucShapeDetectionList.panelBase.buttonAdd.Click()
      Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucShapeDetection.panelBase.txtName.TextBox.Keys(name)
      Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucShapeDetection.panelBase.dropdownDetection.Label.Click(81, 5)
      shape_alias = f"Aliases.ViperVision.ToolStripDropDown.TableLayoutPanel.{detection_name}"
      eval(shape_alias).Click(91,14)
      Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucShapeDetection.panelBase.numLocationAccuracy.RadSpinEditor.HostedTextBoxBase.Keys(str(location_accuracy))
      Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucShapeDetection.panelBase.numLocationAccuracy.RadSpinEditor.wValue = location_accuracy
      
      Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucShapeDetection.panelBase.numSizeAccuracy.RadSpinEditor.HostedTextBoxBase.Keys(str(size_accuracy))
      Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucShapeDetection.panelBase.numSizeAccuracy.RadSpinEditor.wValue = size_accuracy
      
      Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucShapeDetection.panelBase.numCannyThreshold.RadSpinEditor.HostedTextBoxBase.Keys(str(canny_threshold))
      Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucShapeDetection.panelBase.numCannyThreshold.RadSpinEditor.wValue = canny_threshold
      
      Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucShapeDetection.panelBase.VScroll.Pos = 338
      
      Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucShapeDetection.panelBase.numThresholdLinking.RadSpinEditor.HostedTextBoxBase.Keys(str(threshold_linking))
      Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucShapeDetection.panelBase.numThresholdLinking.RadSpinEditor.wValue = threshold_linking
      
      Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucShapeDetection.panelBase.numDetectionFrames.RadSpinEditor.HostedTextBoxBase.Keys(str(detection_frames))
      Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucShapeDetection.panelBase.numDetectionFrames.RadSpinEditor.wValue = detection_frames
      
      Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucShapeDetection.panelButtons.panelOkay.buttonOkay.Click()

      #Aliases.ViperVision.viperSettingsForm.panelBase.panelTop.tlpTop.tlpButtons.buttonClose.ClickButton()
    
      
  def delete_all_rois(self):
    mnu.open_camera()
    mnu.open_camera_roi_center()
    while Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucCameraCenter.tlpButtonControlSplit.panelSettings.ucAllCamerasRois2.panelBase.cardContainerRois.Panel.WaitAliasChild("ViperCard", 1000).Exists:
      mnu.vipercard_roi_remove()
    mnu.close_window()
    
    
  # Validation Functions
  def check_roi_deleted(self, roi: ROI):
    if roi in self.rois:
      tb_info = traceback.format_stack()[-2]
      Log.Error(f"{roi} not deleted\tError occured at: {tb_info}")
      Runner.Stop(True)
    else:
      Log.Message(f"ROI deleted")
  
  def check_all_rois_deleted(self):
    if self.rois:
      tb_info = traceback.format_stack()[-2]
      Log.Error(f"Existing ROIs: ', '.join({self.rois})\tError occured at: {tb_info}")
      Runner.Stop(True)
    else:
      pass
  
  
  '''
  Very misleading function so be aware!!!!!
  Checks the coordinates based off of the camera not the screen coordinates
  roi.x != guru_x
  
  In the meantime use roi_get_coordinates() to get coords relative to its camera
  This is the value that is checked in verify_coordinates()
  '''
  def verify_coordinates(self, roi:ROI, x: int, y: int):
    mnu.open_camera()
    mnu.open_camera_roi_center()
    mnu.vipercard_roi_info()
    x_coord = roi_get_stat(roi.index, "X")
    y_coord = roi_get_stat(roi.index, "Y")
    mnu.close_window()
    mnu.close_window()
    if (x_coord != x) and (y_coord != y):
      tb_info = traceback.format_stack()[-2]
      Log.Error(f"{roi} with coordinates: ({x_coord}, {y_coord})\tError occured at: {tb_info}")
      Runner.Stop(True)
    else:
      Log.Message(f"{roi} verified coordinates with {(x, y)}")
      pass
    
  
  def verify_guru_stat(self, roi:ROI, stat: str, value):
    mnu.open_camera()
    mnu.open_camera_roi_center()
    mnu.vipercard_roi_info()
    guru_value = roi_get_stat(roi.index, stat)
    mnu.close_window()
    mnu.close_window()
    if guru_value != value:
      tb_info = traceback.format_stack()[-2]
      Log.Error(f"{roi} with stat {stat} with value {guru_value}\tError occured at: {tb_info}")
      Runner.Stop(True)
    else:
      Log.Message(f"{roi} verified with stat {stat} and value {guru_value}")
      pass
    
  
  '''
  Be aware that if the ROI is of type spot, then the temperature must change in view at delay
      - Very specific that when delay is over the temperature must be different
  
  Does not work with Ruler ROI
  
  Other ROIs are more lenient depending on their size
  '''
  def verify_streaming(self, roi:ROI, delay: int):
    mnu.open_camera()
    mnu.open_camera_roi_center()
    mnu.vipercard_roi_info()
    avg_temp_now = roi_get_stat(roi.index, "AvgTemp")
    Delay(delay * 1000)
    avg_temp_later = roi_get_stat(roi.index, "AvgTemp")
    mnu.close_window()
    mnu.close_window()
    if avg_temp_now == avg_temp_later:
      tb_info = traceback.format_stack()[-2]
      Log.Error(f"{roi} not detected streaming after {delay / 1000} seconds\tError occured at: {tb_info}")
      Runner.Stop(True)
    else:
      Log.Message(f"{roi} verified streaming after {delay / 1000} seconds")
      pass
    
  
########################### ROI functions ###########################
                    
def roi_get_stat(row: int, column: str):
  mnu.guru_switch_to_roi()
  value = Aliases.ViperVision.viperSettingsForm.panelBase.panelControls.ucGuruMenu.panelBase.tableLayoutPanel1.gridGuru.wValue[row, column]
  return value

def drag_create_roi(roi: ROI):
  if roi.type == ROIType.POLYGON:
    clk.toolbar_click_polygon()
    for x, y in roi.points:
      clk.dock_click(x, y)
    first_point = roi.points[0]
    x_start = first_point[0]
    y_start = first_point[1]
    clk.dock_click(x_start, y_start)
  elif roi.type == ROIType.SPOT:
    clk.toolbar_click_spot()
    clk.dock_click(roi.x, roi.y)
  else:
    x2 = roi.x + roi.width
    y2 = roi.y + roi.height
    if roi.type == ROIType.ELLIPSE:
      clk.toolbar_click_ellipse()
      Aliases.ViperVision.Main.tlpMain.radDockPanel.Drag(roi.x, roi.y, x2, y2)
    elif roi.type == ROIType.ANNULUS:
      clk.toolbar_click_annulus()
      Aliases.ViperVision.Main.tlpMain.radDockPanel.Drag(roi.x, roi.y, x2, y2)
    elif roi.type == ROIType.RECTANGLE:
      clk.toolbar_click_rect()
      Aliases.ViperVision.Main.tlpMain.radDockPanel.Drag(roi.x, roi.y, x2, y2)
    elif roi.type == ROIType.RULER:
      clk.toolbar_click_ruler()
      Aliases.ViperVision.Main.tlpMain.radDockPanel.Drag(roi.x, roi.y, x2, y2)
    else:
      clk.toolbar_click_line()
      Aliases.ViperVision.Main.tlpMain.radDockPanel.Drag(roi.x, roi.y, x2, y2)

# Gets coordinates from specified row  
def roi_get_coordinates(row: int):
  mnu.open_camera()
  mnu.open_camera_roi_center()
  mnu.vipercard_roi_info()
  x = roi_get_stat(row, "X")
  y = roi_get_stat(row, "Y")
  mnu.close_window()
  mnu.close_window()
  return x, y

# Call this to clean up all ROIs and manager but doesnt delete config
def cleanup(manager: ROIManager):
    manager.delete_all_rois()
    del manager
    Log.Message("ROIManager object sucessfully deleted")