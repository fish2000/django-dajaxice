#----------------------------------------------------------------------
# Copyright (c) 2012 David Charbonnier
# All rights reserved.
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met:
#
#    o Redistributions of source code must retain the above copyright
#      notice, this list of conditions, and the disclaimer that follows.
#
#    o Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions, and the following disclaimer in
#      the documentation and/or other materials provided with the
#      distribution.
#
#    o Neither the name of Oxys nor the names of its
#      contributors may be used to endorse or promote products derived
#      from this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY OXYS AND CONTRIBUTORS *AS
#  IS* AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
#  TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
#  PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL DIGITAL
#  CREATIONS OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
#  INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
#  BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS
#  OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
#  ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR
#  TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
#  USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH
#  DAMAGE.
#----------------------------------------------------------------------

from django.core.files.storage import Storage
from dajaxice.core import DajaxiceRequest
from django.template import loader, Context
from django.core.files.temp import NamedTemporaryFile

class DajaxiceStorage(Storage):
    
    def __init__(self):
        self._tmp_file = None #keep reference to avoid tmp file deletion
        
    def _open(self, name, mode='rb'):
        raise NotImplementedError("This backend doesn't support open.")
    
    def save(self, name, content): 
        raise NotImplementedError("This backend doesn't support save.")
    
    def get_valid_name(self, name):
        raise NotImplementedError("This backend doesn't support get_valid_name.")
    
    def get_available_name(self, name):
        raise NotImplementedError("This backend doesn't support get_available_name.")
    
    def path(self, name):
        if name == "":
            return ""
        if name != 'dajaxice/dajaxice.core.js':
            return
        context = Context({'dajaxice_js_functions': DajaxiceRequest.get_js_functions(),
            'DAJAXICE_URL_PREFIX': DajaxiceRequest.get_media_prefix(),
            'DAJAXICE_XMLHTTPREQUEST_JS_IMPORT': DajaxiceRequest.get_xmlhttprequest_js_import(),
            'DAJAXICE_JSON2_JS_IMPORT': DajaxiceRequest.get_json2_js_import(),
            'DAJAXICE_EXCEPTION': DajaxiceRequest.get_exception_message(),
            'DAJAXICE_JS_DOCSTRINGS': DajaxiceRequest.get_js_docstrings()})
        template  = loader.get_template('dajaxice/dajaxice.core.js')
        self._tmp_file = NamedTemporaryFile(suffix='.js')
        self._tmp_file.write(template.render(context))
        self._tmp_file.flush()
        return self._tmp_file.name
    
    def exists(self,path):
        return path == 'dajaxice/dajaxice.core.js'
    
    def listdir(self, path):
        return [], ['dajaxice/dajaxice.core.js']