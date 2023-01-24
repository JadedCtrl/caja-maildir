#
# Copyright (C) 2022, Jaidyn Levesque <jadedctrl@posteo.at>
#
# This program is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#

import os
from sys import argv
import urllib
import email.parser
from dateutil import parser
import mimetypes

from gi.repository import Caja, GObject, Gtk, GdkPixbuf


class Maildir(GObject.GObject,
              Caja.ColumnProvider,
              Caja.InfoProvider):


    def get_columns(self):
        return (
            Caja.Column(
                name="Maildir::from_column",
                attribute="from",
                label="From",
                description=""
            ),
            Caja.Column(
                name="Maildir::subject_column",
                attribute="subject",
                label="Subject",
                description=""
            ),
            Caja.Column(
                name="Maildir::to_column",
                attribute="to",
                label="To",
                description=""
            ),
            Caja.Column(
                name="Maildir::sent_column",
                attribute="sent",
                label="Sent",
                description=""
            )
        )


    def update_file_info(self, file):
        if not file.is_mime_type("message/rfc822"):
            return

        filename = file.get_uri()[7:]
        message = email.message_from_file(open(filename))

        file.add_string_attribute('to', message.get("To"))
        file.add_string_attribute('from', message.get("From"))
        file.add_string_attribute('subject', message.get("Subject"))

        date = parser.parse(message.get("Date"))
        if date:
            file.add_string_attribute('sent', date.strftime("%Y-%m-%d %H:%M:%S %z"))
