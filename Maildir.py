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
import re
from sys import argv
import urllib
import email.parser
from dateutil import parser
import mimetypes

from gi.repository import Caja, GObject, Gtk, GdkPixbuf


class Maildir(GObject.GObject,
              Caja.ColumnProvider,
              Caja.InfoProvider):


    # Pass our columns to Caja
    def get_columns(self):
        return (
            Caja.Column(
                name="Maildir::subject_column",
                attribute="subject",
                label="Subject",
                description=""
            ),
            Caja.Column(
                name="Maildir::sent_column",
                attribute="sent",
                label="Sent",
                description=""
            ),

            Caja.Column(
                name="Maildir::from_column",
                attribute="from",
                label="From",
                description=""
            ),
            Caja.Column(
                name="Maildir::from_addr_column",
                attribute="from_addr",
                label="From (Addr)",
                description=""
            ),
            Caja.Column(
                name="Maildir::from_name_column",
                attribute="from_name",
                label="From (Name)",
                description=""
            ),

            Caja.Column(
                name="Maildir::to_column",
                attribute="to",
                label="To",
                description=""
            ),
            Caja.Column(
                name="Maildir::to_addr_column",
                attribute="to_addr",
                label="To (Addr)",
                description=""
            ),
            Caja.Column(
                name="Maildir::to_name_column",
                attribute="to_name",
                label="To (Name)",
                description=""
            )
        )


    # Implants e-mail-related attributes into a file's columns
    def update_file_info(self, file):
        if not file.is_mime_type("message/rfc822"):
            return

        filename = file.get_uri()[7:]
        message = email.message_from_file(open(filename))

        sender = message.get("From")
        to = message.get("To")
        subject = message.get("Subject")

        if to:
            file.add_string_attribute('to', to)
            file.add_string_attribute('to_addr', self.from_header_addr(to))
            file.add_string_attribute('to_name', self.from_header_name(to))

        if sender:
            file.add_string_attribute('from', sender)
            file.add_string_attribute('from_addr', self.from_header_addr(sender))
            file.add_string_attribute('from_name', self.from_header_name(sender))

        if subject:
            file.add_string_attribute('subject', message.get("Subject"))

        try:
            date = parser.parse(message.get("Date"))
            if date:
                file.add_string_attribute('sent', date.strftime("%Y-%m-%d %H:%M:%S %z"))
        except:
            print("The date couldn't be parsed — that's alright, we didn't need it anyway.")


    # Helper function, for parsing e-mail addresses of to/from headers
    def from_header_addr(self, str):
        if re.search(r'<', str):
            return re.sub('[<|>]', '',
                          re.search(r'<.*@.*>', str).group(0))
        return str


    # Helper function, for parsing names of to/from headers
    def from_header_name(self, str):
        if re.search(r'<', str):
            return re.sub('<.*', '', str)
        return ''
