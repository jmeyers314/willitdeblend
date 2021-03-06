import galsim
import numpy as np
import deblend

bd=galsim.BaseDeviate(1)

def create_blend(peak1, peak2):
    gal1 = galsim.Gaussian(fwhm=1.2, flux=2000.0).shift(peak1).shear(e1=0.1, e2=0.3)
    gal2 = galsim.Gaussian(fwhm=1.8, flux=2500.0).shift(peak2).shear(e1=-0.1, e2=-0.4)
    proto_image = galsim.ImageD(49, 49, scale=0.2)
    image1 = gal1.drawImage(image=proto_image, method='phot', rng=bd)
    #image1 = gal1.drawImage(image=proto_image, method='fft')
    image1.array[np.where(image1.array < 0)] = 0.
    proto_image = galsim.ImageD(49, 49, scale=0.2)
    image2 = gal2.drawImage(image=proto_image, method='phot', rng=bd)
    #image2 = gal2.drawImage(image=proto_image, method='fft')
    image2.array[np.where(image2.array < 0)] = 0.
    return image1+image2, [image1, image2]


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    peak1 = (0.8, 0.2)
    peak2 = (-0.3, 1.26)

    peaks_pix = [[p1/0.2 for p1 in peak1],
                 [p2/0.2 for p2 in peak2]]

    blend, unblends = create_blend(peak1, peak2)
    rot = [deblend.rotate(blend.array, p, interpolate=True) for p in peaks_pix]

    templates, template_fractions, children = deblend.deblend(blend.array, peaks_pix, interpolate=True)

    print blend.array.sum()
    print children[0].sum() + children[1].sum()

    plt.rcParams['xtick.labelsize'] = 6
    plt.rcParams['ytick.labelsize'] = 6
    plt.rcParams['axes.labelsize'] = 8
    plt.rcParams['axes.titlesize'] = 8
    fig = plt.figure(figsize=(8,6.5), dpi=100)
    ax1 = fig.add_subplot(6,4,1)
    ax2 = fig.add_subplot(6,4,2)
    ax3 = fig.add_subplot(6,4,3)
    ax4 = fig.add_subplot(6,4,4)
    ax1.imshow(blend.array, vmin=0, vmax=50)
    ax2.imshow(unblends[0].array, vmin=0, vmax=50)
    ax3.imshow(unblends[1].array, vmin=0, vmax=50)
    ax4.imshow(blend.array != 0, vmin=0, vmax=1)
    ax1.set_title('sum(unblends)')
    ax2.set_title('unblends[0]')
    ax3.set_title('unblends[1]')
    ax4.set_title('nonzero')

    ax6 = fig.add_subplot(6,4,6)
    ax7 = fig.add_subplot(6,4,7)
    ax6.imshow(rot[0], vmin=0, vmax=50)
    ax7.imshow(rot[1], vmin=0, vmax=50)
    ax6.set_title('rot[0]')
    ax7.set_title('rot[1]')

    ax10 = fig.add_subplot(6,4,10)
    ax11 = fig.add_subplot(6,4,11)
    ax12 = fig.add_subplot(6,4,12)
    ax10.imshow(templates[0], vmin=0, vmax=50)
    ax11.imshow(templates[1], vmin=0, vmax=50)
    ax12.imshow((templates[0]+templates[1]) != 0, vmin=0, vmax=1)
    ax10.set_title('templates[0]')
    ax11.set_title('templates[1]')
    ax12.set_title('nonzero')

    ax14 = fig.add_subplot(6,4,14)
    ax15 = fig.add_subplot(6,4,15)
    ax16 = fig.add_subplot(6,4,16)
    ax14.imshow(template_fractions[0], vmin=0, vmax=1)
    ax15.imshow(template_fractions[1], vmin=0, vmax=1)
    ax16.imshow(template_fractions[0]+template_fractions[1], vmin=0, vmax=1)
    ax14.set_title('tfrac[0]')
    ax15.set_title('tfrac[1]')
    ax16.set_title('sum(tfrac)')

    ax18 = fig.add_subplot(6,4,18)
    ax19 = fig.add_subplot(6,4,19)
    ax20 = fig.add_subplot(6,4,20)
    ax18.imshow(children[0], vmin=0, vmax=50)
    ax19.imshow(children[1], vmin=0, vmax=50)
    ax20.imshow(children[0]+children[1], vmin=0, vmax=50)
    ax18.set_title('child[0]')
    ax19.set_title('child[1]')
    ax20.set_title('sum(children)')

    ax22 = fig.add_subplot(6,4,22)
    ax23 = fig.add_subplot(6,4,23)
    ax24 = fig.add_subplot(6,4,24)
    ax22.imshow(unblends[0].array - children[0], vmin=-10, vmax=10)
    ax23.imshow(unblends[1].array - children[1], vmin=-10, vmax=10)
    ax24.imshow(blend.array - (children[0] + children[1]), vmin=-1, vmax=1)
    ax22.set_title('resid[0]')
    ax23.set_title('resid[1]')
    ax24.set_title('total resid')


    fig.tight_layout(pad=1, h_pad=0.1, w_pad=0.1)
    plt.show()
