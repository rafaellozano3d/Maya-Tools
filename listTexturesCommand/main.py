import maya.cmds as cmds
import maya.app.general.fileTexturePathResolver as ftpr

# Save all texture files in a variable
l_files = cmds.ls(type="file")

'''
We iterate around all variable elements for every file node, the
objective its to analyze the "useFrameExtension" attribute, which
indicates if its an animated texture, and the "uvTilingMode", which
contains if its a simple texture or an UDIM texture, depending if its
value is 0 or 3
'''
for s_file in l_files:
    print "\n", s_file, "\n---------------\n"

    # The first step is to get this attributes values, and the file path
    imagePath = cmds.getAttr(s_file + ".fileTextureName")
    tiling_mode = cmds.getAttr(s_file + ".uvTilingMode")
    frame_extension = cmds.getAttr(s_file + ".useFrameExtension")

    # If frame_extension is 1 means that is an animated texture
    if frame_extension == 1:
        print("Type: Animated texture\n")

        # We get the template that Maya use to detect all file set, that is,
        # the part of file name that is repeated
        pattern = ftpr.getFilePatternString(imagePath, True, False)

        # We store all the elements that follow that template
        fileList = ftpr.findAllFilesForPattern(pattern, None)

        # And, finally, to be able to indicate in which frame that texture is
        # displayed, we store the offset, so we will start from frame 0, and we
        # add the offset value to indicate correctly in which frame it is
        offset = cmds.getAttr(s_file + ".frameOffset")
        counter = 0

        # We print on the screen the value of these frame plus the offset, and
        # the path of the file. To access the item, its enough to access the
        # position pointed by the counter, since it increases one by one and
        # start in 0
        for frameImage in fileList:
            print "Frame [", (counter+int(offset)), "]:", fileList[counter]
            counter = counter + 1
    else:

        # If its not animated texture, and its uvTilingMode its 0, that means
        # that its a simple texture, so we only have to print its path
        if tiling_mode == 0:
            print("Type: Simple texture\n")
            print imagePath

        # If its uvTilingMode is 3, it would be an UDIM texture
        if tiling_mode == 3:
            print("Type: UDIM texture\n")
            # We get the part of the name that is repeated
            udim_frame_extension = cmds.getAttr(s_file + ".frameExtension")
            pattern = ftpr.getFilePatternString(imagePath, True, False)
            fileList = ftpr.findAllFilesForPattern(pattern, None)
            counter = 0
            # And we print the name of the files that it has returned to us
            for frameImage in fileList:
                print fileList[counter]
                counter = counter + 1
