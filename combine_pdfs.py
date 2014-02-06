def combine_pdfs(*pdfs, **kwds):
    '''give a list of paths to pdfs, and will combine all into one multi-page pdf file. two optional kwds:
    delete = True (removes the constituent pdfs after merging
    CmbnNm = 'combined' the name of the multi-page pdf file.
    '''
    import subprocess
    import os
    
    # default stuff
    CmbnNm = 'combined'
    delete = True     
    
    # check pdfs arg
    if type(pdfs) is tuple:
        pdfs = list(pdfs)
    elif type(pdfs) is list:
        pass
    else:
        raise TypeError("pdfs is type %s should be list or tuple" % type(pdfs).__name__)

    # parse kwd args
    for kwd,v in kwds.iteritems():
        if kwd=='CmbnNm':
            CmbnNm = v
        if kwd=='delete':
            delete = v
            
    # check kwd args for type and crap, starting to think about C
    if type(CmbnNm) is str:
        CmbnNm = unicode(CmbnNm)
    if type(CmbnNm) is not unicode:
        raise TypeError("combine name is %s should be %s" % (type(CmbnNm).__name__, unicode.__name__))
    if CmbnNm.find('.pdf')>=0:
        pass
    else:
        CmbnNm+='.pdf'

    assert type(delete) is bool, "delete must be bool is %s" % (type(delete).__name__)
    
    # platform stuff
    if os.name=='nt':
        gs_prog_name = 'gswin32c'
    else:
        gs_prog_name = 'gs'

    # make command
    subp_cmd = [gs_prog_name,
                '-dBATCH',
                '-dNOPAUSE',
                '-q',
                '-sDEVICE=pdfwrite',
                "-sOutputFile=%s" % CmbnNm] + pdfs

    subprocess.call(subp_cmd)

    if delete:
        [os.remove(pdf) for pdf in pdfs]
