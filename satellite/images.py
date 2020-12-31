# -*- coding: utf-8 -*-

class ImagingSubsystem(object):
    MAX_PICS = 5

    def __init__(self, power_subsystem):
        super(ImagingSubsystem, self).__init__()
        print("Initilizing Image Subsystem")
        self._pwr = power_subsystem
        self._pictures = [None for x in range(self.MAX_PICS)]
        self._pic_idx = 0

    @property
    def pictures(self):
        return [x for x in self._pictures if x is not None]

    def pop(self):
        for idx, pic in enumerate(self._pictures):
            if pic is not None:
                self._pictures[idx] = None
                break

    def remove_pic(self, pic):
        print("removing pic")
        try:
            idx = self._pictures.index(pic)
            self._pictures[idx] = None
            self._pwr.take_action('picture')
            print("Downloaded {}".format(pic))
        except Exception as e:
            print(e)


    def take_pic(self):
        if self._pwr._power_mode is not "normal":
            print("ERROR: Must be in normal power mode to take pictures")
            return
        if self._pwr._power <= 5:
            print("ERROR: Not enough power to take picture")
            return
        print("Taking a picture")
        self._pictures[self._pic_idx%self.MAX_PICS] = "Pic{}".format(self._pic_idx)
        self._pic_idx += 1
        self._pwr.take_action('picture')
        
    
    def get_tlm(self):
        return {
            "num_pictures": len(self.pictures),
            "pictures": self.pictures,
        }
        
    def list_pics(self):
        return self.pictures 
