from cloudshell.cp.aws.domain.services.parsers.port_group_attribute_parser import PortGroupAttributeParser
from cloudshell.cp.aws.models.port_data import PortData
from cloudshell.cp.aws.domain.services.parsers.custom_param_extractor import VmCustomParamsExtractor


class DeployedAppPortsOperation(object):
    def __init__(self, vm_custom_params_extractor):
        """
        :param VmCustomParamsExtractor vm_custom_params_extractor:
        :return:
        """
        self.vm_custom_params_extractor = vm_custom_params_extractor

    def get_formatted_deployed_app_ports(self, logger, custom_params):
        """
        :param logger: Logger
        :type logger: logging.Logger
        :param custom_params:
        :return:
        """
        logger.info('loading port attributes')
        inbound_ports_value = self.vm_custom_params_extractor.get_custom_param_value(custom_params, "inbound_ports")
        outbound_ports_value = self.vm_custom_params_extractor.get_custom_param_value(custom_params, "outbound_ports")

        if not inbound_ports_value and not outbound_ports_value:
            logger.info('No port attributes found')
            return ""

        result_str_list = []

        logger.info('Parsing inbound ports')
        if inbound_ports_value:
            inbound_ports = PortGroupAttributeParser.parse_port_group_attribute(inbound_ports_value)
            if inbound_ports:
                result_str_list.append("Inbound ports:")
                for rule in inbound_ports:
                    result_str_list.append(self._port_rule_to_string(rule))
                result_str_list.append('')

        logger.info('Parsing outbound ports')
        if outbound_ports_value:
            outbound_ports = PortGroupAttributeParser.parse_port_group_attribute(outbound_ports_value)
            if outbound_ports:
                result_str_list.append("Outbound ports:")
                for rule in outbound_ports:
                    result_str_list.append(self._port_rule_to_string(rule))

        return '\n'.join(result_str_list).strip()

    def _port_rule_to_string(self, port_rule):
        """
        :param PortData port_rule:
        :return:
        """
        if port_rule.from_port == port_rule.to_port:
            port_str = port_rule.from_port
            port_postfix = ""
        else:
            port_str = "{0}-{1}".format(port_rule.from_port, port_rule.to_port)
            port_postfix = "s"

        return "Port{0} {1} {2}".format(port_postfix, port_str, port_rule.protocol)
