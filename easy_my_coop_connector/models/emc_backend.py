# Copyright 2020 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import json
import logging

import requests
from werkzeug.exceptions import NotFound

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class EMCBackend(models.Model):
    _name = "emc.backend"
    _description = "EMC Backend"

    name = fields.Char(string="Name", required=True)
    location = fields.Char(string="Location")
    api_key = fields.Char(string="API Key")
    description = fields.Text(string="Description", required=False)
    active = fields.Boolean(string="active", default=True)

    @api.multi
    def http_get(self, url, params=None, headers=None):
        self.ensure_one()
        headers = self._add_api_key(headers)
        if url.startswith("/"):
            url = self.location + url

        return requests.get(url, params=params, headers=headers)

    @api.multi
    def http_get_content(self, url, params=None, headers=None):
        self.ensure_one()
        response = self.http_get(url, params=params, headers=headers)

        if response.status_code == 200:
            content = response.content.decode("utf-8")
            return json.loads(content)
        else:
            # todo handle different codes (at least 404, 403, 500)
            raise NotFound(
                _("request returned status code %s" % response.status_code)
            )

    @api.multi
    def http_post(self, url, data, headers=None):
        self.ensure_one()
        headers = self._add_api_key(headers)
        if url.startswith("/"):
            url = self.location + url

        return requests.post(url, json=data, headers=headers)

    @api.multi
    def _add_api_key(self, headers):
        self.ensure_one()
        key_dict = {"API-KEY": self.api_key}
        if headers:
            headers.update(key_dict)
        else:
            headers = key_dict
        return headers

    @api.multi
    def action_ping(self):
        self.ensure_one()
        url = self.location + "/api/ping/test"
        try:
            response = requests.get(url)
        except Exception as e:
            _logger.error(e)
            raise Warning(_("Failed to connect to backend: %s" % str(e)))

        if response.status_code == 200:
            content = json.loads(response.content.decode("utf-8"))
            raise Warning(_("Success: %s") % content["message"])
        else:
            raise Warning(
                _("Failed to connect to backend: %s" % str(response.content))
            )

    def run_from_connector_example(self, external_id):
        # this one knows how to speak to emc
        backend_adapter = self.component(usage="backend.adapter")
        # this one knows how to convert emc data to odoo data
        mapper = self.component(usage="import.mapper")
        # this one knows how to link emc/odoo records
        binder = self.component(usage="binder")

        # read external data from emc
        external_data = backend_adapter.read(external_id)
        # convert to odoo data
        internal_data = mapper.map_record(external_data).values()
        # find if the emc id already exists in odoo
        binding = binder.to_internal(external_id)
        if binding:
            # if yes, we update it
            binding.write(internal_data)
        else:
            # or we create it
            binding = self.model.create(internal_data)
        # finally, we bind both, so the next time we import
        # the record, we'll update the same record instead of
        # creating a new one
        binder.bind(external_id, binding)