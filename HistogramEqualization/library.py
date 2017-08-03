import numpy as np

def convertRGB2HSV(image):
    """
        Input image: image[:, :, 0] -> Blue channel
                     image[:, :, 1] -> Green channel
                     image[:, :, 2] -> Red channel
        Output image: newImage[:, :, 0] -> H channel, range[0..255)
                      newImage[:, :, 1] -> S channel, range[0..255]
                      newImage[:, :, 2] -> V channel, range[0..255]
        Formulation:
            (R, G, B) scale from [0..255] to [0..1]
            Cmax = max(R, G, B)
            Cmin = min(R, G, B)
            delta = Cmax - Cmin
                {0                           if delta == 0
            H = {60 * ((G - B)/delta mod 6)  if Cmax  == R
                {60 * ((B - R) / delta + 2)  if Cmax  == G
                {60 * ((R - G) / delta + 4)  if Cmax  == B
            V = Cmax
            S = {0           if Cmax == 0
                {delta/Cmax  if Cmax != 0

    """
    newImage = image.copy()
    for i in xrange(image.shape[0]):
        for j in xrange(image.shape[1]):
            R = 1.0 * image[i, j, 2] / 255.0
            G = 1.0 * image[i, j, 1] / 255.0
            B = 1.0 * image[i, j, 0] / 255.0
            Cmax = np.max([R, G, B])
            Cmin = np.min([R, G, B])
            delta = Cmax - Cmin
            H = 0
            V = Cmax
            if (delta == 0):
                H = 0
            elif (Cmax == R):
                H = 60 * (int((G - B) / delta) % 6)
            elif (Cmax == G):
                H = 60 * ((B - R) / delta + 2)
            else:
                H = 60 *((R - G) / delta + 4)

            if (Cmax == 0):
                S = 0
            else:
                S = delta / Cmax

            newImage[i, j, 0] = int((H / 360) * 255)
            newImage[i, j, 1] = int(S * 255)
            newImage[i, j, 2] = int(V * 255)

    return newImage



def calculateHistogram(image):
    hist = np.array([0] * 256)
    for i in xrange(image.shape[0]):
        for j in xrange(image.shape[1]):
            value = image[i, j]
            hist[value] = hist[value] + 1
    return hist

def histogramEqualization(image, func):
    """
    Theroy:
        s = T(r)
        s: output pixel
        r: input pixel
        T: transform operation
        Theorem:
            P(T(r1) < S <= T(r2)) = P(r1 < S <= r2)
            ps(s)ds = pr(r)dr
            ps(T(r))dT(r)dr = pr(r)dr
            dT(r) = pr(r)dr / ps(T(r))
            T(r) = integrate(0, r) pr(w)dw/ps(w)

            pr: distribution of input
            ps: distribution of output
    """
    hist = calculateHistogram(image) #Calculate histogram input image
    size = 1.0 * image.shape[0] * image.shape[1] #Get number of pixels

    #Transform distribution
    for i in xrange(256):
        hist[i] = hist[i] * 1.0 / func(i)
    for i in xrange(255):
        hist[i + 1] = hist[i] + hist[i + 1]

    #Create output, mapping input pixel to output piexel
    newImage   = image.copy()
    for i in xrange(newImage.shape[0]):
        for j in xrange(newImage.shape[1]):
            newImage[i, j] = np.abs(int(hist[image[i, j]] / size))

    return newImage
